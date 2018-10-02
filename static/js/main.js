      var config = {
            apiKey: "AIzaSyBvwprYXi182UzC0yXiXJXgxXkZ_e68Li0",
            authDomain: "beer2d2-1c27e.firebaseapp.com",
            databaseURL: "https://beer2d2-1c27e.firebaseio.com",
            projectId: "beer2d2-1c27e",
            storageBucket: "",
            messagingSenderId: "109673741253"
        };
        firebase.initializeApp(config);

          var database = firebase.database();

        function login() {
            var provider = new firebase.auth.GoogleAuthProvider();

            firebase.auth().signInWithPopup(provider);
            firebase.auth().getRedirectResult().then(function (result) {
                // if (result.credential) {
                //     // This gives you a Google Access Token. You can use it to access the Google API.
                //     var token = result.credential.accessToken;
                //     // ...
                //     console.log(token)
                //     alert("token:"+ token)
                // }
                // The signed-in user info.
                var user = result.user;
            }).catch(function (error) {
                // Handle Errors here.
                var errorCode = error.code;
                var errorMessage = error.message;
                // The email of the user's account used.
                var email = error.email;
                // The firebase.auth.AuthCredential type that was used.
                var credential = error.credential;
                // ...
                //   alert(error)
            });

                window.location.replace('/dashboard')
        }

        var username = ""
        firebase.auth().onAuthStateChanged((user) => {
            const userProfile = firebase.auth().currentUser;
            if (user) {

                if (/@code.berlin\s*$/.test(userProfile.email)) {
                    // window.open ('dashboard.html','_self',false)
                    console.log("it ends in @code.berlin");
                    console.log(userProfile);
                    username = userProfile.displayName;
                    changeUserButtonText()
                } else {
                    console.log("it doesnt contain @code.berlin");
                    logout();
                }

                // console.log(userProfile);
                // alert('bist eingeloggt Brudi du bist '+firebase.auth().currentUser.displayName);
            }
        })
        // var username = "oh";

        /* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function dropdownPressed() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
