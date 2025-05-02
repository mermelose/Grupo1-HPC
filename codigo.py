import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from datetime import datetime

def extraer_letras_con_espacios(texto):
    """
    Extrae solo letras y espacios de un string, removiendo otros caracteres.
    """
    return ''.join(c for c in texto if c.isalpha() or c.isspace())

def scrape_player_data(player_id):
    """
    Extrae datos de un jugador de Transfermarkt usando su ID.
    """
    url = f'https://www.transfermarkt.pe/player-name/leistungsdaten/spieler/{player_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
   
    # Realizar la solicitud
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanzar excepción si hay error HTTP
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos para el jugador ID {player_id}: {e}")
        return None
   
    # Parsear el contenido HTML
    soup = BeautifulSoup(response.content, 'html.parser')
   
    # Verificar si la página existe y tiene contenido válido
    if "No se ha encontrado la página" in soup.text or "Page not found" in soup.text:
        print(f"Jugador con ID {player_id} no encontrado")
        return None
   
    # Diccionario para almacenar datos del jugador
    player_data = {'id': player_id}
   
    try:
        # Intentar extraer el dorsal (número de camiseta)
        dorsal_element = soup.find('span', class_='data-header__shirt-number')
        player_data['dorsal'] = dorsal_element.text.strip() if dorsal_element else 'N/A'
       
        # Nombre del jugador
        nombre_element = soup.find('h1', class_='data-header__headline-wrapper')
        if nombre_element:
            raw_name = nombre_element.text.strip()
            player_data['nombre'] = extraer_letras_con_espacios(raw_name)
        else:
            player_data['nombre'] = 'N/A'
       
        # Obtener todos los elementos data-header__content
        data_contents = soup.find_all('span', class_='data-header__content')
       
        # Mapear índices de forma segura
        content_mapping = {
            'nacionalidad': 5,
            'edad': 3,
            'altura': 6,
            'posicion': 7
        }
       
        for key, idx in content_mapping.items():
            try:
                player_data[key] = data_contents[idx].text.strip() if len(data_contents) > idx else 'N/A'
            except (AttributeError, IndexError):
                player_data[key] = 'N/A'
       
        # Datos internacionales
        intl_app = soup.find('a', class_='data-header__content data-header__content--highlight')
        player_data['partidos_internacional'] = intl_app.text.strip() if intl_app else '0'
       
        intl_goals = soup.find_all('a', class_='data-header__content data-header__content--highlight')
        player_data['goles_internacional'] = intl_goals[1].text.strip() if len(intl_goals) > 1 else '0'
       
        # Valor de mercado y club
        market_value_element = soup.find('a', class_='data-header__market-value-wrapper')
        player_data['valor_mercado'] = market_value_element.text.strip() if market_value_element else 'N/A'
       
        club_element = soup.find('span', class_='data-header__club')
        player_data['club'] = club_element.text.strip() if club_element else 'N/A'
       
        liga_element = soup.find('span', class_='data-header__league')
        player_data['liga'] = liga_element.text.strip() if liga_element else 'N/A'
       
        # Estadísticas
        zentriert_cells = soup.find_all('td', class_='zentriert')
        rechts_cells = soup.find_all('td', class_='rechts')
       
        player_data['partidos_jugados'] = zentriert_cells[0].text.strip() if zentriert_cells else 'N/A'
        player_data['goles'] = zentriert_cells[1].text.strip() if len(zentriert_cells) > 1 else 'N/A'
        player_data['asistencias'] = zentriert_cells[2].text.strip() if len(zentriert_cells) > 2 else 'N/A'
        player_data['minutos_jugados'] = rechts_cells[1].text.strip() if len(rechts_cells) > 1 else 'N/A'
       
        return player_data
   
    except Exception as e:
        print(f"Error al procesar los datos del jugador ID {player_id}: {e}")
        return None

def format_time(seconds):
    """
    Formatea segundos en horas, minutos y segundos
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
   
    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    elif minutes > 0:
        return f"{int(minutes)}m {int(seconds)}s"
    else:
        return f"{seconds:.2f}s"

def main():
    # Registrar tiempo de inicio
    start_time = time.time()
   
    # Configuración
    start_id = 1  # ID de inicio
    end_id = 100  # ID final
    delay_min = 2  # Tiempo de espera mínimo entre solicitudes (segundos)
    delay_max = 5  # Tiempo de espera máximo entre solicitudes (segundos)
   
    # Nombre del archivo CSV con la fecha/hora actual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f'transfermarkt_players_{timestamp}.csv'
   
    # Lista para almacenar datos de todos los jugadores
    all_players_data = []
    successful_count = 0
   
    print(f"Iniciando extracción de datos para jugadores con ID {start_id} a {end_id}")
    print(f"Usuario: paolosalazarp")
    print(f"Fecha y hora de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
   
    # Recorrer los primeros 100 jugadores por ID
    for player_id in range(start_id, end_id + 1):
        # Tiempo parcial para esta iteración
        iteration_start_time = time.time()
       
        print(f"Procesando jugador ID: {player_id} ({player_id - start_id + 1}/{end_id - start_id + 1})...")
       
        # Extraer datos del jugador
        player_data = scrape_player_data(player_id)
       
        # Si se obtuvieron datos, añadirlos a la lista
        if player_data:
            all_players_data.append(player_data)
            successful_count += 1
            print(f"✓ Datos extraídos exitosamente para {player_data.get('nombre', f'Jugador ID {player_id}')}")
       
        # Calcular tiempo transcurrido en esta iteración
        iteration_time = time.time() - iteration_start_time
        print(f"Tiempo para procesar jugador ID {player_id}: {format_time(iteration_time)}")
       
        # Tiempo total transcurrido hasta ahora
        elapsed_time = time.time() - start_time
        print(f"Tiempo transcurrido total: {format_time(elapsed_time)}")
       
        # Tiempo estimado de finalización
        if player_id > start_id:  # Solo después de procesar al menos 2 jugadores
            avg_time_per_player = elapsed_time / (player_id - start_id + 1)
            remaining_players = end_id - player_id
            estimated_remaining_time = avg_time_per_player * remaining_players
           
            print(f"Tiempo estimado restante: {format_time(estimated_remaining_time)}")
            estimated_completion_time = datetime.now().timestamp() + estimated_remaining_time
            estimated_completion_datetime = datetime.fromtimestamp(estimated_completion_time)
            print(f"Hora estimada de finalización: {estimated_completion_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
       
        # Esperar un tiempo aleatorio entre solicitudes para evitar sobrecarga del servidor
        if player_id < end_id:
            wait_time = random.uniform(delay_min, delay_max)
            print(f"Esperando {wait_time:.2f} segundos antes de la siguiente solicitud...")
            time.sleep(wait_time)
            print("-" * 50)  # Separador para mejor legibilidad
   
    # Guardar datos en CSV
    if all_players_data:
        # Obtener todos los posibles nombres de campo de todos los jugadores
        fieldnames = set()
        for player in all_players_data:
            fieldnames.update(player.keys())
        fieldnames = sorted(list(fieldnames))
       
        # Escribir en CSV
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_players_data)
       
        # Calcular tiempo total
        total_time = time.time() - start_time
       
        print("\n" + "=" * 50)
        print(f"RESUMEN DE LA EXTRACCIÓN")
        print("=" * 50)
        print(f"Fecha y hora de inicio: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Fecha y hora de finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Tiempo total de ejecución: {format_time(total_time)}")
        print(f"Tiempo promedio por jugador: {format_time(total_time / (end_id - start_id + 1))}")
        print(f"Datos guardados exitosamente en '{csv_filename}'")
        print(f"Total de jugadores procesados: {end_id - start_id + 1}")
        print(f"Jugadores con datos extraídos: {successful_count}")
        print(f"Jugadores sin datos: {(end_id - start_id + 1) - successful_count}")
        print(f"Tasa de éxito: {successful_count / (end_id - start_id + 1) * 100:.2f}%")
        print("=" * 50)
    else:
        print("No se pudieron extraer datos de ningún jugador.")

if __name__ == "__main__":
    main()