pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/mlopezm20/prueba_1.git'
        CREDENTIALS_ID = '001'
    }

    stages {
        stage('1. Clonar Repositorio') {
            steps {
                echo 'Obteniendo la última versión de la documentación...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: env.REPO_URL, credentialsId: env.CREDENTIALS_ID]]
                ])
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
                echo 'Ejecutando script de reglas de negocio para Excel y Gherkin...'
                bat 'python ejercicio_prueba.py'
            }
        }
    }

    post {
        success {
            echo '✅ La documentación cumple con todos los estándares definidos por la empresa.'
        }
        failure {
            echo '❌ La revisión extensa falló. Revisa la consola para corregir el archivo Excel o la sintaxis de Gherkin.'
        }
    }
}