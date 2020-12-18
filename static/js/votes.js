
$('.js-vote').click(function(ev){
    ev.preventDefault()
    var $this = $(this),
        action = $this.data('action')
        type = $this.data('type')
        id = $this.data('id')
    $.ajax('/vote_q/', {
        method: 'POST',
        data: {
            action: action,
            type: type,
            id: id,
        },
    }).done(function(data){
        console.log("DATA " + data);
        $('#rating-' + id).text(data.rating);
    });
    console.log("hello " + action + " " + id);
})
