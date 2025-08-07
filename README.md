# Dunk Vision
Dunk Vision is a simple desktop shot-tracking tool for youth basketball players, built with Python and tkinter. 

# Description 
Dunk Vision is a desktop basketball shot tracker and data capture tool built using Python and tkinter. Designed for youth coaches, players, and parents, it lets users: 
- Track individual shot attempts and compare made and missed points
- Visualize performance by court location
- Export shot data for later analysis of team-wide trends
- Develop training insights on individual and team levels

Dunk Vision ensures that whether you are courtside at a state-wide tournament or sitting on the grass at a hectic pickup game, opportunities for structure, data-driven performance insights are always available. 

# Rationale 
Supporting my stepson through middle school basketball, summer camps, youth leagues, and high school basketball it became clear that youth organizations for basketball are propped up by limited funding, parent support, over-stretched coaches, and the goodwill of local communities. 

Jerseys often escape the budget. Lunch is often brought by generous turn-taking parents. Training is often last-minute and inconsistent as coaches balance their personal lives. 

Despite the enthusiasm to participate in this community, I was met with frustration to see my stepson receiving less support than was paid to receive. For this reason, I wanted to build a tool that would turn wild pickup games into structured, targeted training sessions based on the strengths and weaknesses of their previous performances beyond memory or guesswork. I wanted a tool that would support busy coaches to react to the patterns and trends that were missed while juggling parent politics. I wanted a tool that would turn our team that was winning 1 out of every 5 games into a team that stood a chance of winning every time they stepped on the court. 

# Why Dunk Vision?
There are a range of sports analysis tools on the market, but: 
- Key features are locked behind subscriptions that too expensive for schools and youth oranizations
- Basic features like video tagging and analysis are too time-intensive for volunteer parents and coaches 
- Deep geospatial analysis requires multiple camera angles, including overheads
- They focus on a broadcasting service for parents and out-of-town family members

Dunk Vision is designed to complement the use of more sophisticated sports analysis tools by providing rudimentary spatial data without computer vision to suport claims like: "My son is 85% accurate within 15ft, but only 42% accurate after 20ft, so we're cutting back on deep shots until that improves."

# Features 
PLAYER MANAGEMENT 
- Default player profiles based on basketball positions, such as 'Small Forward' and 'Point Guard'
- Rename default player positions to real names, such as 'Point Guard' to 'John Smith', to allow for teams with multiple players filling the same role 
- Insert and delete player profiles
- Users can switch between player profile during a session to track multiple players

GAME MANAGEMENT
- Users should be able to select which quarter they are recording shots for
- Users should be able to mark the game as finished to end the data collection process

SAVING AND LOADING 
- Users can navigate away from the app or minimize the window without losing session data
- Users are warned with a 'Unsaved Data Will Be Lost' when deleting window to allow memory to be cleared
- Users save their partial and complete sessions to local memory
- Users can load saved sessions from local memory
- Users can save player profiles persistently across sessions to prevent re-entering player profiles (useful for tournaments with multiple games in succession)

COURT INTERACTION 
- User selects an area of the court and is met with a color circle gradient to visually confirm touch
- User will receive pop-up box asking if the shot was 'Made', 'Miss', or 'Dunk'
- For 'Made': 
  - If shot was located within the 2pt area, the user selects 'And-1', 'From Rebound', or 'Layup'
  - If shot was located within the 3pt area, the user selects SHOT TYPE? 'Catch and Shoot' or 'Off the Dribble' and then is met with SHOT PRESSURE? 'Contested', 'Wide Open', 'End of Shot Clock'
- For 'Missed':
  - User will be met with 'Airball', 'Rebound', and 'Turnover' as selectable options 
- After 'Made' sequence, the court is painted with a green dot
- After 'Missed' sequence, the court is painted with a red dot
- After 'Dunk' sequence, the court is painted with a gold dot

DISTANCE CALCULATION 
- Court will be zoned into 2pt areas and 3pt areas (three, deep three, corner three)

EXPORT
- User should be able to export the session data in JSON format
- User should be able to export the session in CSV format
- User should be able to export the heatmap as an image

# Future Features
- Color-coding or icons to represent different players on the heatmap, rather than uniform coloring that can be interpreted in the raw file
- Undo button that removes previous entries - dots on the map will not have selection boxes because adding new shots in similar places will be messy
- On selecting 'Game Finished', a pop-up summary of stats will appear presenting user friendly information for each player, selectable through a drop-down menu
- The pop-up summary will feature a 'compare' to assess the stats of two same-team players, where relevant
- Multi-Team Support: Users can load in default player profiles for an opposing team and track opponents shots
- Multi-Team Pop-Up: Users can compare home team summary stats with away team summary stats
- Mult-Team Pop-Up: Users can compare home team player with opposing team player
- On-Screen Score: Tracking home and opposing team scores as shots are tracked
- Switch between half-court view and full-court view at load
- Light mode v dark mode with different court designs for courtside use
- Load files from third-party cloud storage, like OneDrive.
- Add load screen for aesthetics and to address factors like player profiles and light or dark mode before entering

# Use Cases 
- Coaches
  - Identify team trends by analyzing shot location trends to target team-wide strengths and weaknesses to support training
  - Identify player trends by analyzing player shot maps so that bespoke drills and performance goals can be designed
  - Assess opposing teams by preparing solid defensive strategies on an opponent-by-opponent basis by understanding shot behavior
  - Counter individual threats by understanding the patterns of key opposing players for better matchup planning

- Parents
  - College-recruitment support: parents support their players by capturing data during games to provide visual evidence of shot accuracy
  - Compensate youth league gaps: support under-resourced and over-stretched youth leagues with game-changing capabilities  

- Players:
  - Train smarter: Support after-hours training and solo sessions by identifying and improving weak game areas 
  - Bragging rights: do you think you're better than your teammate, or your friends? Prove it with a shotmap and intuitive stats 
 
# Run Instructions 

# Project Structure


# Attributions 
Load Image by Matt Cole on Vecteezy [https://www.vecteezy.com/members/graphicsrf]
Light Mode Court Image by Praeqpailin Phonsri [https://www.vecteezy.com/members/lifestyle-graphic]


# Testing 

# Star This Repo? 
