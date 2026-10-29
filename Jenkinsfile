pipeline {
    agent any


    stages {
        stage('1. Clonar Repositorio') {
            steps {
                echo 'El repositorio ya está en el workspace.'
                bat 'dir'
            }
        }


        stage('2. Preparar Entorno de Validación') {
            steps {
                echo 'Instalando dependencias de Python (openpyxl)...'
                bat '''
                    python -m pip install --upgrade pip
                    python -m pip install openpyxl
                '''
            }
        }


        stage('3. Revisión Extensa de Documentación') {
            steps {
                echo 'Buscando script y archivos Excel...'
                bat '''
                    if not exist validate_docs.py (
                        echo No esta validate_docs.py. No hay nada que revisar.
                        exit /b 0
                    )
                    dir /b *.xlsx *.xls >nul 2>&1
                    if errorlevel 1 (
                        echo No hay archivos Excel en el repositorio. La revision se omite.
                        exit /b 0
                    )
                    python validate_docs.py
                '''
            }
        }
    }


    post {
        success {
            echo 'La documentacion cumple con los estandares, o no habia Excel que revisar.'
        }
        failure {
            echo 'La revision fallo. Revisa la consola.'
        }
    }
}