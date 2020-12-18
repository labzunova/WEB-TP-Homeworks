
$('.js-vote').click(function(ev){
    ev.preventDefault()
    var $this = $(this),
        action = $this.data('action')
        type = $this.data('type')
        id = $this.data('id')
    $.ajax('/vote/', {
        method: 'POST',
        data: {
            action: action,
            type: type,
            id: id,
        },
    }).done(function(data){
        console.log("rating " + data.rating);
        $('#rating-' + id).text(data.rating);
    });
    console.log("hello " + action + " " + id);
})
