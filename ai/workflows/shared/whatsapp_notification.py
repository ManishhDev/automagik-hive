"""
WhatsApp Notification Service for Workflows
==========================================

Provides WhatsApp messaging capabilities for workflow notifications using Agno's MCPTools
to access the Evolution API WhatsApp MCP server. This service handles final typification 
reports, human handoff notifications, and other workflow-generated messages.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from agno.agent import Agent
from agno.tools.mcp import MCPTools
from lib.logging import logger
from lib.exceptions import NotificationError
from lib.config.models import resolve_model, get_default_model_id


def _load_whatsapp_config() -> Dict[str, Any]:
    """Load WhatsApp notification configuration from YAML file."""
    config_path = Path(__file__).parent / "config.yaml"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config.get('whatsapp_notification', {})
    except Exception as e:
        logger.warning("Could not load WhatsApp config, using defaults", error=str(e))
        return {
            'model': {
                'id': get_default_model_id(),
                'provider': 'auto'  # Will be detected by resolver
            },
            'agent': {
                'name': 'WhatsApp Notification Agent',
                'instructions': [
                    "You are a WhatsApp notification agent for the PagBank support system.",
                    "Send professional, concise WhatsApp messages in Portuguese.",
                    "Use the send_whatsapp_message MCP tool to send messages.",
                    "Always include relevant protocol information and next steps.",
                    "Use appropriate emojis for visual clarity.",
                    "Keep messages under 300 words for readability.",
                    "Format messages with proper line breaks and sections."
                ]
            },
            'display': {
                'markdown': True,
                'show_tool_calls': True
            }
        }


class WhatsAppNotificationService:
    """
    WhatsApp notification service using Agno's MCPTools to access Evolution API.
    
    This service creates a specialized agent that can send WhatsApp messages
    for workflow notifications using the Evolution API via MCP integration.
    """
    
    def __init__(self):
        """Initialize WhatsApp notification service."""
        self._agent = None
        self._mcp_tools = None
        logger.debug("WhatsApp notification service initialized")
    
    def _check_notifications_enabled(self) -> bool:
        """Check if WhatsApp notifications are enabled via environment variable."""
        enabled = os.getenv("HIVE_WHATSAPP_NOTIFICATIONS_ENABLED", "false").lower() == "true"
        if not enabled:
            logger.debug("WhatsApp notifications disabled via HIVE_WHATSAPP_NOTIFICATIONS_ENABLED")
            return False
        return True
    
    async def _get_mcp_tools(self):
        """Get simple MCP tools for Evolution API access."""
        # Simple implementation - no pooling needed
        from lib.mcp import get_mcp_tools
        return get_mcp_tools
    
    async def _get_agent(self) -> Agent:
        """Get or create the WhatsApp notification agent with MCP tools."""
        if self._agent is None:
            # Load configuration
            config = _load_whatsapp_config()
            
            # Extract configuration values
            model_config = config.get('model', {})
            agent_config = config.get('agent', {})
            display_config = config.get('display', {})
            
            mcp_tools = await self._get_mcp_tools()
            
            # Use ModelResolver to create model instance
            model_id = model_config.get('id') or get_default_model_id()
            model = resolve_model(model_id)
            
            self._agent = Agent(
                name=agent_config.get('name', 'WhatsApp Notification Agent'),
                model=model,
                tools=[mcp_tools],
                instructions=agent_config.get('instructions', [
                    "You are a WhatsApp notification agent for the PagBank support system.",
                    "Send professional, concise WhatsApp messages in Portuguese."
                ]),
                markdown=display_config.get('markdown', True),
                show_tool_calls=display_config.get('show_tool_calls', True)
            )
        return self._agent
    
    async def send_typification_report(
        self,
        report_data: Dict[str, Any],
        recipient_number: Optional[str] = None
    ) -> None:
        """
        Send final typification report via WhatsApp using Evolution API.
        
        Args:
            report_data: Complete typification report data
            recipient_number: WhatsApp number (optional if env var set)
            
        Raises:
            NotificationError: If message delivery fails
        """
        try:
            # Format the report message
            message = self._format_typification_message(report_data)
            
            # Get the agent with MCP tools
            agent = await self._get_agent()
            
            # Prepare the instruction for the agent
            instruction = self._build_send_instruction(
                message_content=message,
                recipient_number=recipient_number,
                message_type="typification_report"
            )
            
            # Send via WhatsApp agent using MCP tools
            logger.info("📱 Sending typification report via Evolution API", 
                       report_id=report_data.get("report_id"))
            
            # Use simple MCP tools
            get_mcp_tools = await self._get_mcp_tools()
            async with get_mcp_tools("whatsapp_notifications") as tools:
                # Use MCP tools (agno pattern) - get the tool from functions dict
                if "send_text_message" in tools.functions:
                    tool_function = tools.functions["send_text_message"]
                    # Call the MCP tool entrypoint with proper parameters
                    result = await tool_function.entrypoint(None, 
                        instance="SofIA",
                        message=message,
                        number=recipient_number or os.getenv("EVOLUTION_API_FIXED_RECIPIENT")
                    )
                    logger.info("📱 Typification report delivered successfully", 
                               report_id=report_data.get("report_id"))
                else:
                    available_tools = list(tools.functions.keys())
                    raise NotificationError(f"send_text_message tool not available. Available tools: {available_tools}")
            
        except Exception as e:
            logger.error("📱 Critical: Typification report delivery failed", 
                        report_id=report_data.get("report_id"), error=str(e), error_type=type(e).__name__)
            raise NotificationError(f"Typification report delivery failed: {e}") from e
    
    async def send_human_handoff_notification(
        self,
        handoff_data: Dict[str, Any],
        recipient_number: Optional[str] = None
    ) -> None:
        """
        Send human handoff notification via WhatsApp using Evolution API.
        
        Args:
            handoff_data: Human handoff protocol data
            recipient_number: WhatsApp number (optional if env var set)
            
        Raises:
            NotificationError: If message delivery fails
        """
        try:
            # Format the handoff message
            message = self._format_handoff_message(handoff_data)
            
            # Get the agent with MCP tools
            agent = await self._get_agent()
            
            # Prepare the instruction for the agent
            instruction = self._build_send_instruction(
                message_content=message,
                recipient_number=recipient_number,
                message_type="human_handoff"
            )
            
            # Send via WhatsApp agent using MCP tools
            logger.info("📱 Sending human handoff notification via Evolution API",
                       protocol_id=handoff_data.get("protocol_id"))
            
            # Use simple MCP tools
            get_mcp_tools = await self._get_mcp_tools()
            async with get_mcp_tools("whatsapp_notifications") as tools:
                # Use MCP tools (agno pattern) - get the tool from functions dict
                if "send_text_message" in tools.functions:
                    tool_function = tools.functions["send_text_message"]
                    # Call the MCP tool entrypoint with proper parameters
                    result = await tool_function.entrypoint(None, 
                        instance="SofIA",
                        message=message,
                        number=recipient_number or os.getenv("EVOLUTION_API_FIXED_RECIPIENT")
                    )
                    logger.info("📱 Human handoff notification delivered successfully", 
                               protocol_id=handoff_data.get("protocol_id"))
                else:
                    available_tools = list(tools.functions.keys())
                    raise NotificationError(f"send_text_message tool not available. Available tools: {available_tools}")
            
        except Exception as e:
            logger.error("📱 Critical: Human handoff notification delivery failed", 
                        protocol_id=handoff_data.get("protocol_id"), error=str(e), error_type=type(e).__name__)
            raise NotificationError(f"Human handoff notification delivery failed: {e}") from e
    
    def _format_typification_message(self, report_data: Dict[str, Any]) -> str:
        """Format typification report for WhatsApp."""
        try:
            # Extract key information
            typification = report_data.get("typification", {})
            report_id = report_data.get("report_id", "N/A")
            session_id = report_data.get("session_id", "N/A")
            
            # Format hierarchy path
            hierarchy_path = typification.get("hierarchy_path", "N/A")
            
            # Format metrics
            metrics = report_data.get("metrics", {})
            duration = metrics.get("total_duration_minutes", 0)
            customer_messages = metrics.get("customer_messages", 0)
            agent_messages = metrics.get("agent_messages", 0)
            
            # Format satisfaction data
            satisfaction = report_data.get("satisfaction_data", {})
            nps_score = satisfaction.get("nps_score")
            nps_category = satisfaction.get("nps_category", {}).get("value", "N/A")
            
            # Build the message
            message = f"""📊 *Relatório Final de Atendimento*

📋 *Relatório:* {report_id}
🆔 *Sessão:* {session_id}

🎯 *Tipificação:*
{hierarchy_path}

📈 *Métricas:*
⏱️ Duração: {duration:.1f}min
💬 Mensagens: {customer_messages} cliente / {agent_messages} agente"""

            # Add NPS info if available
            if nps_score is not None:
                nps_emoji = "🟢" if nps_score >= 9 else "🟡" if nps_score >= 7 else "🔴"
                message += f"\n⭐ *NPS:* {nps_score}/10 {nps_emoji} ({nps_category})"
            
            # Add escalation info if applicable
            if metrics.get("escalation_triggered"):
                escalation_reason = metrics.get("escalation_reason", "N/A")
                message += f"\n🚨 *Escalado:* {escalation_reason}"
            
            # Add summary
            summary = report_data.get("executive_summary", "Relatório processado com sucesso")
            message += f"\n\n📝 *Resumo:*\n{summary}"
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting typification message: {str(e)}")
            return f"📊 Relatório de Tipificação disponível - ID: {report_data.get('report_id', 'N/A')}"
    
    def _format_handoff_message(self, handoff_data: Dict[str, Any]) -> str:
        """Format human handoff notification for WhatsApp."""
        try:
            # Extract key information
            protocol_id = handoff_data.get("protocol_id", "N/A")
            escalation_analysis = handoff_data.get("escalation_analysis", {})
            
            # Format urgency and emotion
            urgency_level = escalation_analysis.get("urgency_level", "medium")
            customer_emotion = escalation_analysis.get("customer_emotion", "neutral")
            escalation_reason = escalation_analysis.get("escalation_reason", "N/A")
            
            # Map urgency to emoji
            urgency_emoji = {
                "low": "🟢",
                "medium": "🟡", 
                "high": "🟠",
                "critical": "🔴"
            }.get(urgency_level, "⚪")
            
            # Map emotion to emoji
            emotion_emoji = {
                "neutral": "😐",
                "satisfied": "😊",
                "confused": "😕",
                "frustrated": "😤",
                "angry": "😠",
                "urgent": "😰"
            }.get(customer_emotion, "😐")
            
            # Format reason in Portuguese
            reason_map = {
                "explicit_request": "Solicitação explícita",
                "frustration_detected": "Frustração detectada",
                "complex_issue": "Problema complexo",
                "high_value": "Alto valor envolvido",
                "security_concern": "Questão de segurança",
                "multiple_attempts": "Múltiplas tentativas",
                "system_limitation": "Limitação do sistema"
            }
            reason_pt = reason_map.get(escalation_reason, escalation_reason)
            
            # Build the message
            message = f"""🚨 *Escalação para Atendimento Humano*

📋 *Protocolo:* {protocol_id}
🎯 *Prioridade:* {urgency_level.upper()} {urgency_emoji}
😊 *Emoção:* {customer_emotion} {emotion_emoji}
📝 *Motivo:* {reason_pt}

⏰ *Tempo de resposta:* 15-30 minutos
📞 *Equipe:* Atendimento especializado

Um atendente entrará em contato em breve.
Obrigado pela paciência!"""
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting handoff message: {str(e)}")
            return f"🚨 Escalação para atendimento humano - Protocolo: {handoff_data.get('protocol_id', 'N/A')}"
    
    def _build_send_instruction(
        self,
        message_content: str,
        recipient_number: Optional[str] = None,
        message_type: str = "notification"
    ) -> str:
        """Build instruction for WhatsApp agent using Evolution API."""
        
        # Use Evolution API environment variable if no recipient specified
        if not recipient_number:
            recipient_number = os.getenv("EVOLUTION_API_FIXED_RECIPIENT")
            
        if not recipient_number:
            logger.warning("No WhatsApp recipient specified and no default configured")
            recipient_number = "5511999999999@s.whatsapp.net"  # Fallback number
        
        # For Evolution API, we need to use the MCP tool properly
        instruction = f"""Use the send_whatsapp_message tool to send the following {message_type} message.

Instance: {os.getenv("EVOLUTION_API_INSTANCE", "SofIA")}
Recipient: {recipient_number}
Message: {message_content}

Please send this message now using the send_whatsapp_message tool and confirm delivery."""
        
        return instruction
    
    async def send_custom_message(
        self,
        message: str,
        recipient_number: Optional[str] = None,
        message_type: str = "custom"
    ) -> None:
        """
        Send custom WhatsApp message using Evolution API.
        
        Args:
            message: Custom message content
            recipient_number: WhatsApp number (optional if env var set)
            message_type: Type of message for logging
            
        Raises:
            NotificationError: If message delivery fails or notifications disabled
        """
        # Check if WhatsApp notifications are enabled
        if not self._check_notifications_enabled():
            logger.warning("📱 WhatsApp notifications disabled", message_type=message_type)
            raise NotificationError("WhatsApp notifications disabled via HIVE_WHATSAPP_NOTIFICATIONS_ENABLED")
        
        try:
            # Get the agent with MCP tools
            agent = await self._get_agent()
            
            # Prepare the instruction for the agent
            instruction = self._build_send_instruction(
                message_content=message,
                recipient_number=recipient_number,
                message_type=message_type
            )
            
            # Send via WhatsApp agent using MCP tools
            logger.info("📱 Sending custom WhatsApp message via Evolution API",
                       message_type=message_type)
            
            # Use simple MCP tools
            get_mcp_tools = await self._get_mcp_tools()
            async with get_mcp_tools("whatsapp_notifications") as tools:
                # Use MCP tools (agno pattern) - get the tool from functions dict
                if "send_text_message" in tools.functions:
                    tool_function = tools.functions["send_text_message"]
                    # Call the MCP tool entrypoint with proper parameters
                    result = await tool_function.entrypoint(None, 
                        instance="SofIA",
                        message=message,
                        number=recipient_number or os.getenv("EVOLUTION_API_FIXED_RECIPIENT")
                    )
                    logger.info("📱 Custom message delivered successfully", message_type=message_type)
                else:
                    available_tools = list(tools.functions.keys())
                    raise NotificationError(f"send_text_message tool not available. Available tools: {available_tools}")
            
        except Exception as e:
            logger.error("📱 Critical: Custom message delivery failed", 
                        message_type=message_type, error=str(e), error_type=type(e).__name__)
            raise NotificationError(f"Custom message delivery failed: {e}") from e


# Global instance for easy access
_whatsapp_service = None

def get_whatsapp_notification_service() -> WhatsAppNotificationService:
    """Get or create the global WhatsApp notification service."""
    global _whatsapp_service
    
    if _whatsapp_service is None:
        _whatsapp_service = WhatsAppNotificationService()
    
    return _whatsapp_service


async def send_workflow_notification(
    notification_type: str,
    data: Dict[str, Any],
    recipient_number: Optional[str] = None
) -> None:
    """
    Convenience function to send workflow notifications via WhatsApp using Evolution API.
    
    Args:
        notification_type: Type of notification ('typification_report', 'human_handoff', 'custom')
        data: Notification data
        recipient_number: Optional WhatsApp number
        
    Raises:
        NotificationError: If notification delivery fails or unknown type
    """
    # Check if WhatsApp notifications are enabled
    enabled = os.getenv("HIVE_WHATSAPP_NOTIFICATIONS_ENABLED", "false").lower() == "true"
    if not enabled:
        logger.warning("📱 WhatsApp notifications disabled globally", notification_type=notification_type)
        raise NotificationError("WhatsApp notifications disabled via HIVE_WHATSAPP_NOTIFICATIONS_ENABLED")
    
    service = get_whatsapp_notification_service()
    
    if notification_type == "typification_report":
        await service.send_typification_report(data, recipient_number)
    elif notification_type == "human_handoff":
        await service.send_human_handoff_notification(data, recipient_number)
    elif notification_type == "custom":
        await service.send_custom_message(
            data.get("message", ""),
            recipient_number,
            data.get("message_type", "custom")
        )
    else:
        logger.error("📱 Unknown notification type requested", notification_type=notification_type)
        raise NotificationError(f"Unknown notification type: {notification_type}")