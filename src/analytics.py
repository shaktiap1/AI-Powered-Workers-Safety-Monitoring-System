# SAFETY ANALYTICS - this class is responsible for collecting and analyzing data related to worker posture and safety events detected during the video processing.

class SafetyAnalytics: 
    def __init__(self):
        self.total_frames = 0
        self.total_people = 0

        self.posture_counts = {
            "Standing": 0,
            "Sitting": 0,
            "Bending": 0
        }

        self.risk_events = 0

    def update(self, boxes, postures, safety_states): # this method takes the detected bounding boxes, classified postures, and safety states for each person in the current video frame as input.
                                                     #  It updates the total frame count, total people count, posture distribution counts, and risk event count based on the provided data. 
                                                     # The posture_counts dictionary is updated by incrementing the count for each detected posture type (Standing, Sitting, Bending), while the risk_events counter is incremented for each person classified as being in a "RISK" safety state.
                                                     #  This method allows the SafetyAnalytics class to maintain a running summary of the posture and safety data across all processed video frames, which can later be used to generate a comprehensive analytics report.
    
        self.total_frames += 1
        self.total_people += len(boxes)

        for posture in postures: 
            if posture in self.posture_counts:
                self.posture_counts[posture] += 1

        for state in safety_states:
            if state == "RISK":
                self.risk_events += 1

    def generate_report(self, output_path="outputs/analytics_report.txt"): # this method generates a comprehensive analytics report summarizing the posture distribution and safety events detected during the video processing. 
                                                                           # It calculates the percentage distribution of each posture type (Standing, Sitting, Bending) based on the total number of detected postures 
                                                                           # and compiles this information along with the total frames processed, total people detected, and total risk events into a formatted report string.
                                                                           # Finally, it saves this report to a specified text file path and prints a confirmation message indicating where the analytics report has been saved.
        """
        Save analytics summary to a text file.
        """
        total_postures = sum(self.posture_counts.values())

        if total_postures == 0:
            total_postures = 1

        standing_pct = (self.posture_counts["Standing"] / total_postures) * 100
        sitting_pct = (self.posture_counts["Sitting"] / total_postures) * 100
        bending_pct = (self.posture_counts["Bending"] / total_postures) * 100

        report = f"""

                    SAFETY ANALYTICS REPORT 


                    Total Frames Processed: {self.total_frames}
                    Total Person Detections: {self.total_people}

                    Posture Distribution:
                    Standing: {self.posture_counts['Standing']} ({standing_pct:.2f}%)
                    Sitting : {self.posture_counts['Sitting']} ({sitting_pct:.2f}%)
                    Bending : {self.posture_counts['Bending']} ({bending_pct:.2f}%)

                    Total Risk Events Detected: {self.risk_events}

                """

        with open(output_path, "w") as f: # this will open a text file at the specified output path in write mode and save the generated analytics report string to that file.  
            f.write(report)

        print("\nAnalytics report saved to:", output_path)

# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH
