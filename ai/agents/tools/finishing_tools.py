# Finishing Tools for Finalizacao Specialist Agent
# Tools for conversation finalization, protocol retrieval, and farewell messages

from typing import Dict, Any, Optional
from agno.tools import tool
from agno.utils.log import logger

# Import shared protocol utilities
from ai.workflows.shared.protocol_generator import (
    get_protocol_from_session_state,
    format_protocol_for_user
)

# Import existing workflow
from ai.workflows.conversation_typification.workflow import get_conversation_typification_workflow


@tool
def trigger_conversation_typification_workflow(
    session_id: str,
    conversation_history: str,
    customer_message: str,
    customer_id: Optional[str] = None
) -> str:
    """
    Trigger the conversation typification workflow to generate protocol.
    
    This tool executes the complete 5-level typification process and generates
    a protocol that gets saved to session state for later retrieval.
    
    Args:
        session_id: Session identifier
        conversation_history: Complete conversation history
        customer_message: Final customer message
        customer_id: Customer identifier (optional)
        
    Returns:
        Status message about typification completion
    """
    
    logger.info(f"🎯 Triggering conversation typification for session {session_id}")
    
    try:
        # Create and run typification workflow using factory function
        workflow = get_conversation_typification_workflow()
        
        # Execute workflow with proper input format for Agno Workflows 2.0
        results = list(workflow.run(
            message=conversation_history,
            session_id=session_id,
            customer_id=customer_id
        ))
        
        if not results:
            logger.error("🚨 Typification workflow returned no results")
            return "❌ Erro na tipificação: Nenhum resultado obtido"
        
        # Get the final result
        final_result = results[-1]
        
        # Extract protocol information from the result
        if hasattr(final_result, 'metadata') and final_result.metadata:
            protocol_info = final_result.metadata.get('protocol_info', {})
            protocol_id = protocol_info.get('protocol_id')
            
            if protocol_id:
                logger.info(f"✅ Typification completed successfully with protocol: {protocol_id}")
                return f"✅ Tipificação concluída com sucesso! Protocolo: {protocol_id}"
            else:
                logger.warning("⚠️ Typification completed but no protocol ID found")
                return "⚠️ Tipificação concluída, mas protocolo não encontrado"
        else:
            logger.warning("📊 Typification completed but no metadata found")
            return "✅ Tipificação concluída com sucesso!"
            
    except Exception as e:
        logger.error(f"❌ Typification workflow failed: {str(e)}")
        return f"❌ Erro na tipificação: {str(e)}"




@tool
def send_farewell_message(
    protocol_id: str,
    customer_name: Optional[str] = None,
    message_type: str = "standard"
) -> str:
    """
    Send personalized farewell message with protocol information.
    
    Args:
        protocol_id: Protocol identifier to include in message
        customer_name: Customer name for personalization
        message_type: Type of farewell message (standard, grateful, professional)
        
    Returns:
        Formatted farewell message
    """
    
    logger.info(f"💬 Sending farewell message for protocol {protocol_id}")
    
    try:
        # Format protocol for user display
        protocol_message = format_protocol_for_user({
            "protocol_id": protocol_id,
            "protocol_type": "finalization"
        })
        
        # Create personalized farewell message
        if customer_name:
            if message_type == "grateful":
                farewell = f"Obrigado por entrar em contato, {customer_name}! Fico feliz em ter ajudado. {protocol_message}. Tenha um ótimo dia!"
            elif message_type == "professional":
                farewell = f"Atendimento finalizado para {customer_name}. {protocol_message}. Agradecemos!"
            else:  # standard
                farewell = f"Obrigado por entrar em contato, {customer_name}! Seu atendimento foi finalizado com sucesso. {protocol_message}. Tenha um ótimo dia!"
        else:
            if message_type == "grateful":
                farewell = f"Fico feliz em ter ajudado! {protocol_message}. Agradecemos!"
            elif message_type == "professional":
                farewell = f"Atendimento finalizado com sucesso. {protocol_message}. Agradecemos pela preferência!"
            else:  # standard
                farewell = f"Seu atendimento foi finalizado com sucesso! {protocol_message}. Obrigado!"
        
        logger.info(f"✅ Farewell message created successfully")
        return farewell
        
    except Exception as e:
        logger.error(f"❌ Failed to create farewell message: {str(e)}")
        return f"❌ Erro ao criar mensagem de despedida: {str(e)}"


