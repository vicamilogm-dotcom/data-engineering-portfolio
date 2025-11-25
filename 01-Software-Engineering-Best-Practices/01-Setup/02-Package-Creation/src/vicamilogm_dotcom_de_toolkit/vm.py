import click
import subprocess



VM_NAME = "lewagon-data-eng-vm-victorg"     
VM_ZONE = "us-central1-c"                
VM_USER = "vicamilogm"                       
VM_IP = "35.232.192.205"                     
REMOTE_PATH = f"/home/vicamilogm/code/vicamilogm-dotcom"     


def run_cmd(cmd: list[str]) -> None:
    """Ejecuta un comando del sistema y muestra stdout/stderr."""
    print(f"→ Ejecutando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


@click.command()
def start():
    """Iniciar vm"""
    cmd = [
        "gcloud",
        "compute",
        "instances",
        "start",
        f"--zone={VM_ZONE}",
        VM_NAME,
    ]
    run_cmd(cmd)
    print("✅ VM iniciada correctamente")


@click.command()
def stop():
    """Parar vm"""
    cmd = [
        "gcloud",
        "compute",
        "instances",
        "stop",
        f"--zone={VM_ZONE}",
        VM_NAME,
    ]
    run_cmd(cmd)
    print("✅ VM detenida correctamente")


@click.command()
def connect():
    """Connect to your vm in vscode inside your ~/code/<user>/folder"""
    # URI especial para VSCode Remote SSH
    folder_uri = (
        f"vscode-remote://ssh-remote+{VM_USER}@{VM_IP}{REMOTE_PATH}"
    )

    cmd = [
        "code",
        "--folder-uri",
        folder_uri,
    ]
    run_cmd(cmd)
    print("✅ VSCode intentando conectar a la VM (Remote SSH)")
