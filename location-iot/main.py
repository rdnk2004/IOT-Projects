import sys
from iss_collector import collect_iss_data
from iss_analyzer import analyze_iss_data

def main():
    print("==================================================")
    print("      REAL-TIME ISS LOCATION ANALYSIS SYSTEM      ")
    print("==================================================")
    
    csv_file = "iss_location_data.csv"
    sample_count = 100
    sample_interval = 5
    
    # Check if arguments provided
    if len(sys.argv) > 1:
        try:
            sample_count = int(sys.argv[1])
        except ValueError:
            pass
            
    # Step 1: Collect Data
    collect_iss_data(total_records=sample_count, interval_seconds=sample_interval, output_file=csv_file)
    
    # Step 2: Analyze & Plot Data
    metrics = analyze_iss_data(csv_path=csv_file)
    
    print("\nWorkflow completed successfully!")

if __name__ == "__main__":
    main()
