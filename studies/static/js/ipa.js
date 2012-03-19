if ($==undefined){
    $ = django.jQuery;
}
$(document).ready(function(){
    $('.output').each(function (e) {
        var self = $(this);
        $.ajax({url: '/keyboard/',
                data: {"input_id": self.attr("id")},
                success: function(payload){
                    self.parent().append(payload);
                    initialise();
                },
                dataType: 'html',
                type: 'get',
        });
    });
});
function localInitialise(){}

function viewKeyboards(){
    document.getElementById('keyboards').style.display = 'inline-block';
}
