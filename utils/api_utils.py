import re
import ollama



def parse_state_changes(response_text: str, current_state: dict) -> dict:
    """
    Parse the AI's response to extract state changes (HP and inventory modifications)
    Returns a dictionary with the updated state values
    """
    state_changes = current_state.copy()
    
    # Encontra a seção após as últimas opções numeradas (1., 2., 3., etc)
    sections = response_text.split('\n')
    last_option_idx = -1
    for i, line in enumerate(sections):
        if line.strip().startswith(('1.', '2.', '3.')):
            last_option_idx = i
    
    if last_option_idx >= 0 and last_option_idx + 1 < len(sections):
        # Pega apenas o texto após as opções
        status_text = '\n'.join(sections[last_option_idx + 1:]).lower()
    else:
        status_text = response_text.lower()
    
    # Parse HP changes - procura por padrões exatos
    hp_changes = re.findall(r'-(\d+)\s*(?:pontos de vida|hp)', status_text)
    hp_healing = re.findall(r'\+(\d+)\s*(?:pontos de vida|hp)', status_text)
    
    # Apply HP changes
    for damage in hp_changes:
        state_changes['hp'] = max(0, state_changes['hp'] - int(damage))
    for healing in hp_healing:
        state_changes['hp'] = min(100, state_changes['hp'] + int(healing))
    
    # Parse inventory changes - usando os verbos exatos especificados
    gain_verbs = r'(?:pegou|obteve|encontrou|recebeu|ganhou)'
    lose_verbs = r'(?:perdeu|usou|consumiu|gastou)'
    
    items_gained = re.findall(f'{gain_verbs}\\s+([^.,!?\\n]+)', status_text)
    items_lost = re.findall(f'{lose_verbs}\\s+([^.,!?\\n]+)', status_text)
    
    # Apply inventory changes
    for item in items_gained:
        item = item.strip()
        if item not in state_changes['inventory']:
            state_changes['inventory'].append(item)
    
    for item in items_lost:
        item = item.strip()
        if item in state_changes['inventory']:  # Só remove se o item existir no inventário
            state_changes['inventory'].remove(item)
    
    return state_changes



def gerar_narrativa(action, state):

    rpg_prompt = f"""
                Você é um mestre de RPG experiente, narrando aventuras em português brasileiro.
                Continue a história com base na ação do jogador: '{action}'.
                Contexto atual:
                - Pontos de Vida (HP): {state['hp']}
                - Inventário: {state['inventory']}
                - Últimas cenas: {state['history'][-2:] if len(state['history']) > 0 else "Nenhuma"}
                - Cena atual: {state['current_scene']}
                Gere de 1 a 2 parágrafos narrativos mantendo o clima de aventura, fantasia e coerência com o cenário. Ao final dos 1 a 2 parágrafos acabe em uma escolha para o jogador, fazendo-o tomar uma ação.
                
                **IMPORTANTE:**
                - Sempre interaja com o HP e o inventário quando houver eventos relevantes
                - Alterações no HP ou inventário devem estar fundamentadas em eventos da história
                - Após as opções, informe mudanças usando exatamente este formato:
                  Dano: "-X pontos de vida" ou "-X hp"
                  Cura: "+X pontos de vida" ou "+X hp"
                  Itens ganhos: "pegou/obteve/encontrou/recebeu/ganhou [item]"
                  Itens perdidos: "perdeu/usou/consumiu/gastou [item]"
                
                O jogador só pode usar itens que estão no inventário.
                Mantenha o clima de fantasia medieval e seja consistente com o mundo apresentado.
                """

    resposta = ollama.generate(
        model="qwen3:0.6b",
        prompt=action,
        system=rpg_prompt,
        options={
            "temperature": 1, 
            "frequency_penalty": 0.8,
            "top_k": 30,
            "presence_penalty": 0.8,
        },
        
    )



    return resposta['response']


