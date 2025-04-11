from crew.crew_setup import AutoDevCrew

def main():
    # Initialize the crew
    crew = AutoDevCrew()
    
    # Example task
    task = "Create a Python script that fetches weather data and plots it."
    
    # Run the crew
    result = crew.run(task)
    print("\n🎉 Final Result:")
    print(result)

if __name__ == "__main__":
    main()
