import subprocess

def get_gpu_usage():
    try:
        result = subprocess.check_output(["rocm-smi", "--showuse"]).decode("utf-8")
        lines = result.splitlines()
        for line in lines:
            if "GPU" in line:  # Suche nach einer Zeile, die die GPU-Daten enthält
                parts = line.split()
                # Überprüfen, ob genügend Teile vorhanden sind
                if len(parts) > 4:
                    return parts[4]  # Beispiel: GPU-Auslastung ist der dritte Wert
        return "Keine GPU-Daten gefunden"
    except subprocess.CalledProcessError as e:
        return f"Fehler: {e}"
    except IndexError as e:
        return f"Indexfehler: {e}"

gpu_usage = get_gpu_usage()
print(f"GPU-Auslastung: {gpu_usage}")
