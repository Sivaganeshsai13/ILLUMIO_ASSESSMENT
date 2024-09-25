import csv
import os

# Step 1: Load the lookup table
def load_lookup_table(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} does not exist.")
        return {}

    lookup = {}
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Create a key from dstport and protocol (in lowercase to make it case-insensitive)
                key = (row['dstport'], row['protocol'].lower())
                lookup[key] = row['tag']  # Store the tag for the combination
    except Exception as e:
        print(f"Error loading lookup table: {e}")
    return lookup

# Step 2: Parse flow logs and count matches
def parse_flow_logs(log_filename, lookup):
    tag_count = {}
    port_protocol_count = {}
    untagged_count = 0

    if not os.path.exists(log_filename):
        print(f"Error: {log_filename} does not exist.")
        return {}, {}, 0

    with open(log_filename, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) < 8:  # Ensure there are enough parts to avoid index errors
                print(f"Skipping malformed line: {line}")
                continue

            dstport = parts[5]
            protocol_number = str(parts[7])

            
            if protocol_number == '6':
                protocol = 'tcp'
            elif protocol_number == '17':
                protocol = 'udp'
            else:
                protocol = 'unknown'
                
            print(f"Extracted protocol number: {protocol_number}")

            key = (dstport, protocol)
            tag = lookup.get(key, 'Untagged')

            if tag == 'Untagged':
                untagged_count += 1
            else:
                tag_count[tag] = tag_count.get(tag, 0) + 1

            port_protocol_key = (dstport, protocol)
            port_protocol_count[port_protocol_key] = port_protocol_count.get(port_protocol_key, 0) + 1

    return tag_count, port_protocol_count, untagged_count

# Step 3: Write results to output file
def write_output(tag_count, port_protocol_count, untagged_count, output_filename):
    try:
        with open(output_filename, 'w') as file:
            # Write Tag Counts
            file.write("Tag Counts:\nTag,Count\n")
            for tag, count in tag_count.items():
                file.write(f"{tag},{count}\n")
            file.write(f"Untagged,{untagged_count}\n")

            # Write Port/Protocol Combination Counts
            file.write("\nPort/Protocol Combination Counts:\nPort,Protocol,Count\n")
            for (port, protocol), count in port_protocol_count.items():
                file.write(f"{port},{protocol},{count}\n")
    except Exception as e:
        print(f"Error writing output: {e}")

# Main function to run the whole process
def main():
    lookup_table_file = 'lookup.csv'  # Path to lookup table
    flow_log_file = 'flow_logs.txt'   # Path to flow logs
    output_file = 'output.txt'        # Output file path

    lookup = load_lookup_table(lookup_table_file)  # Load the lookup table
    tag_count, port_protocol_count, untagged_count = parse_flow_logs(flow_log_file, lookup)  # Parse flow logs
    write_output(tag_count, port_protocol_count, untagged_count, output_file)  # Write the output
    print(f"Results written to {output_file}")

if __name__ == "__main__":
    main()
