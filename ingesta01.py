import boto3
import psycopg2
import csv

# Parámetros de conexión PostgreSQL
db_host = "34.237.90.249"
db_user = "postgres"
db_password = "utec"
db_name = "estudiantes_y_inscripciones"
db_port = 5432
postgres_tables = ["estudiantes", "inscripciones"]

# Parámetros para S3
nombre_bucket = "proyecto-uni"
s3_client = boto3.client('s3')

def export_postgres_to_csv(table_name):
    conexion = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    resultados = cursor.fetchall()

    fichero_upload = f"{table_name}_postgres.csv"
    with open(fichero_upload, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])
        writer.writerows(resultados)

    cursor.close()
    conexion.close()
    
    # Subir archivo a S3
    s3_client.upload_file(fichero_upload, nombre_bucket, fichero_upload)
    print(f"Ingesta completada y archivo {fichero_upload} subido a S3.")

def main():
    for table in postgres_tables:
        export_postgres_to_csv(table)

if __name__ == "__main__":
    main()
