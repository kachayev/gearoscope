
var setQueueStates = function(){
    $('#queues_list .queue_item').each(function(){
        if($(this).hasClass('collapsed')){
            collapseQueue(this);
        }else{
            expandQueue(this);
        }
    });

    $('#queues_list .expand_queue').live('click', function(e){
        e.preventDefault();
        expandQueue(this);
    });

    $('#queues_list .collapse_queue').live('click', function(e){
        e.preventDefault();
        console.log('opa');
        collapseQueue(this);
    });
};

var collapseQueue = function(el){
    var item = $(el);

    if(! $(el).hasClass('queue_item')){
        item = $(el).parents('.queue_item');
    }
    $(item).addClass('collapsed').find('.collapse_queue').hide().end().find('.expand_queue').show();

};

var expandQueue = function(el){
    var item = $(el);
    if(! $(el).hasClass('queue_item')){
        item = $(el).parents('.queue_item');
    }
    $(item).removeClass('collapsed').find('.collapse_queue').show().end().find('.expand_queue').hide();

};


var initStubs = function(){

    $('.add_worker').live('click', function(e) {
        e.preventDefault();
        alert("Add worker not ready yet.");
    });

    $('.stop_worker, .restart_worker, .delete_worker').live('click', function(e) {
        e.preventDefault();
        alert("Add worker not ready yet.");
    });
    
};


$(document).ready(function(){

    initStubs();

    setQueueStates();

});
