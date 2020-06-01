# env2repo

<p align="center">
  <img src="https://github.com/YatinAdityaT/env2repo/blob/master/assets/icon.png" width="200"> 
</p>
:grin: A TKinter GUI that help you backup your environments to GitHub/delete them and much more.

## Motivation:
<p align="center">
  <img src="https://github.com/YatinAdityaT/env2repo/blob/master/docs/100gb.png" width="300" > 
</p>
Creating conda envs is a good habit. It help in keeping project dependencies separate and makes our lives a lot easier by helping us avoid dependency conflicts. But these envs hog up a lot of space. And if you are one of those unlucky people who naively installed Anaconda on their "C" drives (like me) then you will be aware of that feeling of dread when any software tries to install something on that drive (even though you specified it to use the "D" drive :frowning_face:) which is already choked up with the 10 envs you don't use anymore but can't let go.

I have an embracing amount of envs on my system. Manually backing up each one to GitHub and then deleting them is super tedious and boring and would take hours.

So in a true developer fashion I made this GUI in a couple of days instead :sweat_smile:. 

## Requirements:
- Conda installed on system and its path variable added to environment variables
- Git installed on system and its path variable added to environment variables


## Demo:
<p align="center">
  <img src="https://github.com/YatinAdityaT/env2repo/blob/master/docs/env2repo.gif" width="900">
</p>


## Usage:
- Create an empty repo on GitHub. Make sure not to initialise any README or other files in it. Copy its URL.
- Clone this repo
- Run the .exe file 
- Paste the URL in the textbox and hit "Enter URL"
- This will automatically clone your GitHub repo on your local machine
- In the "Your envs" tab you should be able to see the envs on your system.
- In the "Envs on GitHub" tab you will see the envs you have saved.
- In the "Your envs" tab select on any env of your choice and hit "Check if backedup". This will check if a backup of the selected env exists on GitHub. It will also check if the env has been modified later on will notify the user appropriately.
- "Backup env" backs up an env on GitHub.
- "Delete env" removes the env from your local machine and **not from GitHub**. It warns the user if a backup doesn't exist on GitHub or if the env has been updated later on.
- In the "Envs on GitHub" tab you should see all envs you have on GitHub. "Open" will open the selected env in a file browser. Inside the env you should see folders with numbers on them (0,1,2...) these indicate the version number.
- **Every backup creates a new version folder and doesn't override the previous backup**
- Inside these version folders you should see two .yml files. One is created by running ```conda env export --name {env} > temp.yml``` and the other by running ```conda env export --from-history --name {env} > {file_path_from_history}```.
- **"Delete env" in the "Envs on GitHub" tab deletes entire env backup from GitHub. But doesn't affect the env locally**


- **To install from yml file**: Use the command: `conda env create -f environment.yml` as specified [here](https://github.com/conda/conda/issues/3417#issuecomment-247109058) or `conda env update --file environment.yaml --name dropSeqPipe` as specified [here](https://github.com/conda/conda/issues/6827#issuecomment-365562719) intead of `conda install --file` as shown [here](https://github.com/conda/conda/issues/6827#issuecomment-365614464).

## Caution:
- Read the warning/alert messages carefully if you don't want to lose your envs.

## Known issues:
- GUI hangs and shows "Not responding" when git is working in the background.

## How to contribute:

### Directly
- Fork this repo
- Create a new branch (leave the master untouched)
- Do your stuff in this branch
- Start a pull request

### Indirectly
- Use this software and report any bugs you find in the issues section.

## Authors:
- Yatin Aditya Tekumalla - [YatinAdiyaT](https://github.com/YatinAdityaT)

## License:
This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details
