import pyrebase

firebase_config = {
    "apiKey": "AIzaSyAOYUEm5lxZ7hAzWVKwWDfzse7xxFaAojs",
    "authDomain": "cliniforge.firebaseapp.com",
    "projectId": "cliniforge",
    "storageBucket": "cliniforge.firebasestorage.app",
    "messagingSenderId": "701219592084",
    "appId": "1:701219592084:web:03514d9addc6eed076a181",
    "measurementId": "G-C8S67V6L3B",
    "databaseURL": ""
};

def signup(email, password):
    return auth.create_user_with_email_and_password(email, password)


def login(email, password):
    return auth.sign_in_with_email_and_password(email, password)

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()