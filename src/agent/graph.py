from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import retrieve, grade_documents, generate

# inicializa o grafo
workflow = StateGraph(AgentState)

workflow.add_node("recuperador", retrieve)
workflow.add_node("avaliador", grade_documents)
workflow.add_node("gerador", generate)

workflow.set_entry_point("recuperador")
workflow.add_edge("recuperador", "avaliador")
workflow.add_edge("avaliador", "gerador")
workflow.add_edge("gerador", END)

app_agente = workflow.compile()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("INICIADO".center(50))
    print("="*50)
    
    while True:
        pergunta = input("\nFaça uma pergunta ao Agente (ou 'sair'): ")
        if pergunta.lower() == 'sair':
            break
        
        print("\n" + "-"*30)
        # injetamos a pergunta inicial no State
        resultado = app_agente.invoke({"question": pergunta})
        
        print("\nRESPOSTA FINAL:")
        print(resultado["answer"])
        print("-" * 50)