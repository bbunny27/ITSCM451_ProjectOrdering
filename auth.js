const poolData = {
  UserPoolId: 'us-east-2_xp99YsAGM',
  ClientId: '62p0ogqpctgd29qoj9aptrqk4j'
};

const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

window.login = function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  const authDetails = new AmazonCognitoIdentity.AuthenticationDetails({
    Username: username,
    Password: password,
  });

  const user = new AmazonCognitoIdentity.CognitoUser({
    Username: username,
    Pool: userPool
  });

  user.authenticateUser(authDetails, {
    onSuccess: function(result) {
      const idToken = result.getIdToken().getJwtToken();
      localStorage.setItem("idToken", idToken);
      console.log("✅ Login successful. Token stored.");
      window.location.href = "shop.html";
    },
    onFailure: function(err) {
      document.getElementById('msg').innerText = "Login failed: " + err.message;
    }
  });
}

window.signup = function signup() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  userPool.signUp(username, password, [], null, function(err, result) {
    if (err) {
      document.getElementById('msg').innerText = "Signup failed: " + err.message;
    } else {
      document.getElementById('msg').innerText = "Signup successful! Please log in.";
    }
  });
}
