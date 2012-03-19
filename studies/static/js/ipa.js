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
                    var anchor = $("<A>");
                    anchor.attr("href", "javascript:void(0);");
                    anchor.attr("id");
                    anchor.attr("class", "keyboard");
                    anchor.text("Keyboard");
                    anchor.click(function(e) {
                        $("#phoneticKeyboard").toggle();
                    });
                    self.parent().append(anchor);
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
