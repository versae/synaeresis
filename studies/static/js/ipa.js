if ($==undefined){
    $ = django.jQuery;
}
$(document).ready(function(){
    $('.ipakey').each(function (e) {
        var self = $(this);
        $.ajax({url: '/keyboard/',
                data: {"input_id": self.attr("id")},
                success: function(payload){
                    var anchor = $("<A>");
                    anchor.attr("href", "javascript:void(0);");
                    anchor.attr("id");
                    anchor.attr("class", "keyboard");
                    anchor.text("Keyboard");
                    anchor.click(function(e) {
                        self.parent().find("#phoneticKeyboard").toggle();
                    });
                    self.parent().addClass("parent");
                    self.parent().append(anchor);
                    self.parent().append(payload);
                    //debugger;
                    initialise((self.parent()).get(0));
                },
                dataType: 'html',
                type: 'get',
        });
    });
});
function localInitialise(){}

function viewKeyboards(_button){
    $(_button).parents('#phoneticKeyboard').find('#keyboards').get(0).style.display = 'inline-block';
}
