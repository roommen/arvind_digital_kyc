
/* Show Recommendations */
function showRecommendation(){
        //API Endpoint - Replace this with endpoint you created
        var reco_url = 'https://llneei56ca.execute-api.ap-south-1.amazonaws.com/arvind/showrecommendations';
         $.ajax({
             url: reco_url,
             type: 'GET',
             async: false,
             success: function(result)
            {
                reco_success = result['reco'];
                console.log(reco_success);
                html_code = "";
                if(reco_success === "true"){
                    r1 = result['r1'];
                    r2 = result['r2'];
                    r3 = result['r3'];
                    r4 = result['r4'];
                    r5 = result['r5'];
                    html_code += '<tr><td>' + r1 + '</td></tr><tr><td>' + r2 + '</td></tr><tr><td>' + 
                    r3 + '</td></tr><tr><td>' + r4 + '</td></tr><tr><td>' + r5 + '</td></tr>';
                }else{
                    html_code += '<tr><td>reco1</td></tr><tr><td>reco2</td></tr><tr><td>reco3</td></tr><tr><td>reco4</td></tr><tr><td>reco5</td></tr>';
                }
                $('#reco-list thead').html(html_code);
            },
         });
}
