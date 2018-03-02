
/* Calculate Loyalty Points & Show Recommendation */
function calculateLoyaltyShowRecommendation(phone){
    if(phone) {
        //Calculate random loyalty points between 50 and 150
        min = 50;
        max = 150;
        points = Math.floor(Math.random()*(max-min+1)+min)
        $("#error").text("*You've accumulated " + points + " points");
        $("#error").css('visibility', 'visible');
        $("#phone").val("");
    }
    else {
        $("#error").text("*Please enter your mobile number");
        $("#error").css('visibility', 'visible');
        $("#phone").val("");
    }
}
