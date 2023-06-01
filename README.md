#MHSN-Project
made by Matthew Tujague, class of 2023:

DIRECTIONS FOR UPLOADING EVENTS:
This is the workflow for the MHSN Dashboard that allows for communication between different websites, and the transmission of web data to the actual website,
such web data also include MHSN Dashboard events! If you are to upload/delete an event, please follow these directions...

1) If the program is running, click on the output tab, if one does not exist, you can pop it up by finding it in the tools section on your screen
2) If the screen is not black, skip to step 7, otherwise, click the stop button, then click run once more,
3) If after waiting the screen in output is still black, please go to the filebar on the left hand corner, go to main.py, otherwise go to step 7
4) When you arrive at main.py, scroll down to line 120, highlight lines 120-121, control+/ to comment them out, they should be green
5) Click stop at the top if the programming is running
6) After having commented out the lines, navigate to the tools section and click on shell, inside of the shell paste this, "python3 main2.py"
7) When you renavigate to the output tab, follow the directions on the MHSN Event Editor,
8) if you have had to use steps 2-6, when you finish editing events, IT IS VITAL YOU UNCOMMENT OUT LINES 120-121 IN MAIN.PY
9) To do this, go back to main.py in the filebar, highlight lines 120-121, and use control+/ once more, the lines should be white/colorful but not green
10) You have successfully used the MHSN Event Editor!

Summary:
Sends back to MSHNDash required information to put up on the screen via HTTP, has an integrated Event Editor GUI for uploading/deleting events
on the dashboard.

Requirements: 
```
- python == 3.8
- lxml == 4.6.3
- beautifulsoup4 == 4.9.3
- flask == 2.0.1
```