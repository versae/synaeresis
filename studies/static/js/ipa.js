if ($==undefined){
    $ = django.jQuery;
}
$(document).ready(function(){
    $.ajax({url: 'http://localhost:8000/studies/ipa_keyboard/',
            success: function(payload){
                $('#output').parent().append(payload);
                initialise();
            },
            dataType: 'html',
            type: 'get',});
});
function localInitialise(){}

function viewKeyboards(){
    document.getElementById('keyboards').style.display = 'inline-block';
}
