
## USED TO GO BEHIND THE GOOGLE JS
$.ajax({
        headers: {"X-CSRFToken": token},
        processData: false,
        contentType: false,
        url: '/studentview/',
        data: email,
        type: 'POST',
        success: function(response) { // Go through appliction if does work then prints
            print(response)
            console.log("it works, God save the Queen!");
        },
    });
}





            $(document).on("click", '#login', function(e) {
                $(document).ready(function() {
                    var data = {
                        'email': 'filter_city',
                        'id_A': "FGDKJ"
                    };
                    $.ajax({
                        url: '/login_request/',
                        data: data,
                        type: 'GET',
                        success: function(response) { // Go through appliction if does ork then prints
                            console.log(response);
                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
                });
            })

            $(document).ready(function() {
                var data = {
                    'email': 'filter_city',
                    'id_A': "FGDKJ",
                };
                $.ajax({
                    url: '/login_request/',
                    data: data,
                    type: 'GET',
                    success: function(response) { // Go through appliction if does ork then prints
                        console.log(response);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            });