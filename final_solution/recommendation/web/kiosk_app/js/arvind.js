
/* Calculate Loyalty Points */
function calculateLoyalty(phone){
    if(phone) {
        //API Endpoint - Replace this with endpoint you created
        loyalty_url = 'https://llneei56ca.execute-api.ap-south-1.amazonaws.com/arvind/insertloyaltycheck';
        var obj = new Object();
        obj.phone = phone;

        var jsonObj = JSON.stringify(obj);

        $.ajax({
            url: loyalty_url,
            type: 'PUT',
            data: jsonObj,
            dataType: 'json',
            success: function(result)
            {
                loyalty_success = result['update'];
                if(loyalty_success === "true"){
                    min = 50;
                    max = 150;
                    points = Math.floor(Math.random()*(max-min+1)+min)
                    $("#error").text("*You've accumulated " + points + " points");
                    $("#error").css('visibility', 'visible');
                    $("#phone").val("");
                }else{
                    $("#error").text("*There seems to be some error");
                    $("#error").css('visibility', 'visible');
                    $("#phone").val("");
                }
            },
        });
    }
    else {
        $("#error").text("*Please enter your mobile number");
        $("#error").css('visibility', 'visible');
        $("#phone").val("");
    }
}
