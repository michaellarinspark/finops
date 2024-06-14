import csv
import os

# Define the path to the folder containing the CSV files
csv_folder_path = "C://Users//micha//OneDrive - Spark New Zealand//Vendors//AWS//bills"

# Get a list of all the CSV files in the folder
csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]

# Create a temporary CSV file to store the combined data
combined_csv_file_path = os.path.join(os.getcwd(), "temp_combined_csv.csv")

# Combine all CSV files
with open(combined_csv_file_path, "w", newline='') as combined_csv_file:
    csv_writer = csv.writer(combined_csv_file)

    header_written = False

    for csv_file in csv_files:
        with open(os.path.join(csv_folder_path, csv_file), "r") as input_csv_file:
            csv_reader = csv.reader(input_csv_file)
            header = next(csv_reader)  # Read the header from the current CSV file

            if not header_written:
                csv_writer.writerow(header)  # Write header only once
                header_written = True

            for row in csv_reader:
                csv_writer.writerow(row)

# Create the final CSV file with parsed UsageType for specific ProductName
final_combined_csv_file_path = os.path.join(csv_folder_path, "combined_csv_with_usagetype.csv")

# Function to handle parsing of the UsageType column
def parse_usagetype(product_name, usage_type):
    region = 'undefined'
    meter_name = 'undefined'
    meter_subcategory = 'undefined'
    meter_size = 'undefined'

    match (product_name):
        case 'Amazon API Gateway':
            parts = usage_type.split('-')
            region = parts[0]
            meter_name = parts[1]
            meter_subcategory = ''
            meter_size = ''
        case 'Amazon Athena':
            parts = usage_type.split('-')
            region = parts[0]
            meter_name = parts[1]
            meter_subcategory = ''
            meter_size = ''
        case 'Amazon Bedrock':
            parts = usage_type.split('-')
            region = parts[0]
            meter_name = parts[1]
            meter_subcategory = parts[2]
            meter_size = parts[3] + '-' + parts[4]
        case 'Amazon CloudFront':
            parts = usage_type.split('-')
            if len(parts) == 0:    
                region = ''
                meter_name = usage_type
                meter_subcategory = ''
                meter_size = ''
            elif len(parts)== 1:
                region = ''
                meter_name = usage_type
                meter_subcategory = ''
                meter_size = ''
            elif len(parts) == 2:
                region = ''
                meter_name = parts[0]
                meter_subcategory = parts[1]
                meter_size = ''
            elif len(parts) == 3:
                if parts[0] == 'Lambda':
                    region = ''
                    meter_name = parts[0]
                    meter_subcategory = parts[1]
                    meter_size = parts[2]
                else:
                    region = parts[0]
                    meter_name = parts[1]
                    meter_subcategory = parts[2]
                    meter_size = ''
            elif len(parts) == 4:
                if parts[0] == 'Lambda':
                    region = ''
                    meter_name = parts[0]
                    meter_subcategory = parts[1]
                    meter_size = parts[2] + '-' + parts[3]
                else:
                    region = parts[0]
                    meter_name = parts[1]
                    meter_subcategory = parts[2]
                    meter_size = parts[3]
            elif len(parts) == 5:
                region = parts[0]
                meter_name = parts[1]
                meter_subcategory = parts[2]
                meter_size = parts[3] + '-' + parts[4]
        case 'Amazon Cognito':
            parts = usage_type.split('-')
            region = parts[0]
            meter_name = parts[1]
            meter_subcategory = ''
            meter_size = ''
        case 'Amazon Comprehend':
            parts = usage_type.split('-')
            region = parts[0]
            meter_name = parts[1]
            meter_subcategory = ''
            meter_size = ''
        case 'Amazon DynamoDB':
            parts = usage_type.split('-')
            if len(parts[0]) > 4:
                region = ''
                meter_name = parts[0]
                meter_subcategory = parts[1]
                meter_size = ''
            elif len(parts) == 3 :
                region = parts[0]
                meter_name = parts[1]
                meter_subcategory = parts[2]
                meter_size = ''
            else:
                region = parts[0]
                meter_name = parts[1]
                meter_subcategory = ''
                meter_size = ''
        case 'Amazon EC2 Container Registry (ECR)':
            parts = usage_type.split('-')
            region = parts[0]
            meter_name = parts[1]
            meter_subcategory = parts[2]
            meter_size = ''
        case 'Amazon Elastic Compute Cloud':
            dash = usage_type.split('-')
            colon = usage_type.split(':')
            dot = usage_type.split('.')
            print(f"dash {len(dash)} colon {len(colon)} dot {len(dot)}")
            if len(dash) == 1:
                if len(colon) > 0 and len(dot) > 0:
                    region = ''
                    meter_name = colon[0]
                    meter_subcategory = colon[1]
                    meter_size = str(len(dash)) +' '+ str(len(colon)) +' '+ str(len(dot))
                    #meter_size = dot[2]
                elif len(colon) > 2 and len(dot) == 0:
                    region = ''
                    meter_name = colon[0]
                    meter_subcategory = colon[1]
                    meter_size = str(len(dash)) +' '+ str(len(colon)) +' '+ str(len(dot))
                    #meter_size = ''
            elif len(dash) == 2:
                if len(colon) > 0 and len(dot) > 1:
                    region = dash[0]
                    meter_name = colon[0].replace(dash[0] + '-','')
                    meter_subcategory = colon[1].replace('.' + dot[1],'')
                    #meter_size = dot[1]
                    meter_size = str(len(dash)) +' '+ str(len(colon)) +' '+ str(len(dot))
                elif len(colon) > 0 and len(dot) == 0:
                    region = dash[0]
                    meter_name = colon[0].replace(dash[0] + '-','')
                    meter_subcategory = colon[1]
                    meter_size = str(len(dash)) +' '+ str(len(colon)) +' '+ str(len(dot))
                    #meter_size = ''
            elif len(dash) == 3 and len(dot) > 1:
                if dot[1] == 'piops':
                    region = dash[0]
                    meter_name = colon[0].replace(dash[0] + '-','')
                    meter_subcategory = colon[1].replace(dot[1],'')
                    meter_size = str(len(dash)) +' '+ str(len(colon)) +' '+ str(len(dot))
                    #meter_size = ''
                else:
                    region = dash[0]
                    meter_name = dash[1]
                    meter_subcategory = dash[2]
                    meter_size = str(len(dash)) +' '+ str(len(colon)) +' '+ str(len(dot))
                    #meter_size = ''
            else:
                region = 'undefined'
                meter_name = 'undefined'
                meter_subcategory = 'undefined'
                meter_size = str(len(dash)) +' '+ str(len(colon)) +' '+ str(len(dot))
        case _:
            pass

    return region, meter_name, meter_subcategory, meter_size

# Parse the combined CSV and add the new columns
with open(combined_csv_file_path, "r", newline='') as combined_csv_file, \
     open(final_combined_csv_file_path, "w", newline='') as final_csv_file:

    csv_reader = csv.reader(combined_csv_file)
    csv_writer = csv.writer(final_csv_file)

    header = next(csv_reader)  # Read the header from the combined CSV
    usagetype_index = header.index('UsageType') if 'UsageType' in header else None
    productname_index = header.index('ProductName') if 'ProductName' in header else None

    if usagetype_index is not None and productname_index is not None:
        header.extend(['Region', 'MeterName', 'MeterSubcategory', 'MeterSize'])

    csv_writer.writerow(header)  # Write the modified header to the final CSV file

    for row in csv_reader:
        if usagetype_index is not None and productname_index is not None:
            product_name = row[productname_index]
            usage_type = row[usagetype_index]
            region, meter_name, meter_subcategory, meter_size = parse_usagetype(product_name, usage_type)
            row.extend([region, meter_name, meter_subcategory, meter_size])
        csv_writer.writerow(row)

# Remove the temporary combined CSV file
os.remove(combined_csv_file_path)

print(f"Combined CSV files successfully exported to {final_combined_csv_file_path}.")
