
$('.js-correct').click(function(ev){
    ev.preventDefault()
    var $this = $(this),
        qid = $this.data('qid')
        aid = $this.data('aid')
    $.ajax('/correct/', {
        method: 'POST',
        data: {
            qid: qid,
            aid: aid,
        },
    }).done(function(data){
       // console.log("rating " + data.rating);
       $('#correct-' + aid).prop( "checked", true );
       $('#correct-' + data.old_correct).prop( "checked", false );
    });
    console.log("hello " + action + " " + id);
})
