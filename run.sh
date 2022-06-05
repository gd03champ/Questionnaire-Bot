#rasa main server activate
rasa run -m models --enable-api --cors "*"

#rasa action server activate
rasa run actions

#navigate to react app location
cd react && cd app 

#start react app for front-end
npm start