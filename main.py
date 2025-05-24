import json
from utils.api_utils import gerar_narrativa, parse_state_changes
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.text import Text
import time
import os
from rich.padding import Padding


console = Console()


SAVE_FILE = "game_state.json"


def load_game(save_file: str = "game_state.json") -> dict:
    """
    Carrega o estado do jogo a partir de um arquivo JSON.
    Retorna o estado carregado ou o estado inicial se o arquivo não existir.
    """
    try:
        save_path = Path(save_file)
        if not save_path.exists():
            raise FileNotFoundError
        
        with open(save_path, 'r', encoding='utf-8') as f:
            loaded_state = json.load(f)
        
        # Validação básica do estado carregado
        required_keys = {'hp', 'inventory', 'history', 'current_scene'}
        if not all(key in loaded_state for key in required_keys):
            raise ValueError("Arquivo de save corrompido")
            
        return loaded_state
        
    except FileNotFoundError:
        console.print("[INFO] Save não encontrado, iniciando novo jogo", justify='center')
        return get_initial_state()
    except (json.JSONDecodeError, ValueError) as e:
        console.print(f"[bold red][ERRO] Save corrompido: {e}[/bold red]. Iniciando novo jogo")
        return get_initial_state()


def save_game(state: dict, save_file: str = "game_state.json") -> bool:
    """
    Salva o estado do jogo em um arquivo JSON.
    Retorna True se bem-sucedido, False caso contrário.
    """
    try:
        save_path = Path(save_file)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        return True
    except (IOError, TypeError) as e:
        print(f"[ERRO] Falha ao salvar jogo: {e}")
        return False


def get_initial_state() -> dict:
    """Retorna um estado inicial limpo do jogo"""
    return {
        "hp": 100,
        "inventory": ["espada", "poção de cura"],
        "history": [],
        "current_scene": "Você acorda em um floresta velha..."
    }


def print_status(state):
    console.print(f'Inventário: {state["inventory"]}', justify='left')
    console.print(f'\n[bold green]HP -> {'[X]'*(state['hp']//10)}[/bold green][bold red]{'[ ]'*(10 - state['hp']//10)}[/bold red]  [bold green][[bold red]{state['hp']}[/bold red]/100][/bold green]', justify='left')


def display_typing_effect(text, color="cyan", justify="left"):
    """Display text with a typing effect using Rich"""
    width = console.width
    with Live(auto_refresh=False, console=console) as live:
        for i in range(len(text) + 1):
            content = Text(text[:i], style=color, justify=justify)
            # Add padding to ensure consistent width
            padded = Padding(content, (0, 1))
            live.update(padded, refresh=True)
            time.sleep(0.01)
    print()  # Add final newline


def main():

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen initially

    state = load_game()

    console.print("[bold green]Bem-vindo ao RPG![/bold green] \n", justify="center")

    display_typing_effect(state['current_scene'], color="yellow", justify="center")
    print("\n")

    print_status(state)

    while state['hp'] > 0:
        action = input("\n> O que você faz? ")

        if action == 'quit':
            break

        if action == 'reset':
            state = get_initial_state()
            save_game(state)
            break

        # Get narrative from local Ollama model
        narrative = gerar_narrativa(action, state)

        # Parse state changes from the narrative
        updated_state = parse_state_changes(narrative, state)
        state.update(updated_state)
        
        print("\n")  # Add some spacing
        display_typing_effect(narrative, justify="full")
        print("\n")  # Add some spacing

        print_status(state)

        state['history'].append(narrative)
        state['current_scene'] = narrative
        save_game(state)

    console.print("\n[bold red]Fim do jogo![/bold red]", justify="center")


if __name__ == "__main__":
    print('\n\n\n')
    main()