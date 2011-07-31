


var initStubs = function(){

    $('.add_worker').live('click', function(e) {
        e.preventDefault();
        queue.setQueue(this).setData().update();
    });

    $('.stop_worker, .restart_worker, .delete_worker').live('click', function(e) {
        e.preventDefault();
        worker.setItem(this).setData().update();
    });
    
};

var showAllWorkers = function(e){
    if (typeof e != 'undefined'){
        e.preventDefault();
    }
    var item = $(this);
    if(! $(item).hasClass('queue_item')){
        item = $(item).parents('.queue_item');
    }
    $(item).find('.worker_details').each(function(){
        $(this).find('worker_stats').show().end().find('graph_holder').show().end().find('.small_stats').hide();
    });
};

var worker = {
    item: null,
    data: null,
    counter: 0,
    is_null: function(){
        return typeof (this.item) != 'object';
    },
    collapse: function(){
        if (this.is_null){
            return false;
        }
        this.item.find('worker_stats').hide().end().find('graph_holder').hide().end().find('.small_stats').show();
        return this;
    },
    expand: function(){
        if (this.is_null){
            return false;
        }
        this.item.find('worker_stats').show().end().find('graph_holder').show().end().find('.small_stats').hide();
        return this;
    },
    setItem: function(el){
        if($(el).hasClass('.worker_details')){
            this.item = el;
        }else{
            this.item = $(el).parents('.worker_details');
        }
        return this;
    },

    appendPoint: function(points, key, value){
        if(typeof points == 'undefined'){
            points = [];
        }
        if(typeof(value) == 'undefined'){
            value = 0;
        }
        points.push([key, value]);
        points = points.slice(-30);
        return points;
    },
    
    update: function(){
        var wdata = $(this.item).data('worker-data');
        wdata = this.data;
        console.log(wdata);
        $(this.item).find('.worker_stats .cpu_value').html('' + wdata.cpu_value + '%').end()
            .find('.worker_stats .mem_value').html('' + wdata.memory_value + '%').end()
            .find('.worker_stats .task_value').html(wdata.task_value).end();

        $(this.item).find('.worker_stats .cpu.progress').width(Math.min(Math.max(wdata.cpu_value, 1), 99)+'%');
        $(this.item).find('.worker_stats .memory.progress').width(Math.min(Math.max(wdata.memory_value, 1), 99)+'%');

        var counter = this.counter;

        var cpu_points = this.appendPoint($(this.item).data('cpu-points'), counter, wdata.cpu_value);
        $(this.item).data('cpu-points', cpu_points);
        
        var mem_points = this.appendPoint($(this.item).data('memory-points'), counter, wdata.memory_value);
        $(this.item).data('memory-points', mem_points);

        var task_points = this.appendPoint($(this.item).data('task-points'), counter, wdata.task_value);
        $(this.item).data('task-points', task_points);

        this.counter = counter + 1;

        console.log(counter);

        $.plot($(this.item).find('.graph_holder'), [
            {
                data: cpu_points,
                lines: {show:true, fill:true},
                color: "rgb(0,255,0)"
            },{
                data: mem_points,
                lines: {show:true, fill:true},
                color: "rgb(22,150,255)"
            },{
                data: task_points,
                lines: {show:true, fill:true},
                color: "rgb(255,232,37)"
            }
        ]);

        return this;
    },
    
    setData: function(){
        //this is stub
        var d = {
            cpu_value: Math.round(Math.random() * 100),
            memory_value: Math.round(Math.random() * 100),
            task_value: Math.round(Math.random() * 10 + 20)
        };
        this.data = d;
        $(this.item).data('worker-data', d);

        return this;
    }
};

var queue = {
    item : null,
    is_null: function(){
        return typeof (this.item) != 'object';
    },

    setQueue: function(el){
        if($(el).hasClass('queue_item')){
            this.item = el;
        }else{
            this.item = $(el).parents('.queue_item');
        }
        return this;
    },

    collapseWorkers:function(){
        $(this.item).find('.worker_details').each(function(){
            worker.setItem(this).collapse();
        });
        return this;
    },

    expandWorkers:function(){
        $(this.item).find('.worker_details').each(function(){
            worker.setItem(this).expand();
        });
        return this;
    },

    expand: function(){
        $(this.item).removeClass('collapsed').find('.collapse_queue').show().end().find('.expand_queue').hide();
    },

    collapse: function(){
        $(this.item).addClass('collapsed').find('.collapse_queue').hide().end().find('.expand_queue').show();
    },

    isCollapsed: function(){
        return $(this.item).hasClass('collapsed');
    },

    update: function(){
        var qdata = $(this.item).data('queue-data');
        $(this.item).find('.queue_stats .cpu_value, .queue_headline .cpu_value').html('' + qdata.cpu_value + '%').end()
            .find('.queue_stats .mem_value, .queue_headline .mem_value').html('' + qdata.memory_value + '%').end()
            .find('.queue_stats .workers_value, .queue_headline .workers_value').html(qdata.workers_value).end();

        $(this.item).find('.queue_stats .cpu.progress').width(Math.min(Math.max(qdata.cpu_value, 1), 99)+'%');
        $(this.item).find('.queue_stats .memory.progress').width(Math.min(Math.max(qdata.memory_value, 1), 99)+'%');
        return this;
    },

    initGraph: function(){
        
    },

    setData: function(){
        //this is stub
        var d = {
            cpu_value: Math.round(Math.random() * 100),
            memory_value: Math.round(Math.random() * 100),
            workers_value: Math.round(Math.random() * 10)
        };
        
        $(this.item).data('queue-data', d);
        
        return this;
        
    },

    init: function(){
        $('#queues_list .queue_item').each(function(){
            var q = queue.setQueue(this);
            if(q.isCollapsed()){
                q.collapse();
            }else{
                q.expand();
            }
        });

        $('#queues_list .expand_queue').live('click', function(e){
            e.preventDefault();
            queue.setQueue(this).expand();
        });
        
        $('#queues_list .collapse_queue').live('click', function(e){
            e.preventDefault();
            queue.setQueue(this).collapse();
        });

        $('.expand_all').click(function(e){
            e.preventDefault();
            $('#queues_list .queue_item').each(function(){
                queue.setQueue(this).expand();
            });
        });
    }
};


var servers = {

    data: null,
    template_log: 'serverLog',
    template_item: 'serverLogItem',

    setData: function(data){
        this.data = data;
        return this;
    },
    
    update: function(){
        var serverList = $('#servers').find('#servers_list');
        serverList.find('li').remove();

        for(i in this.data){
            var server = this.data[i];
            var li = $.tmpl(this.template_log, {name:i});

            if(server.length > 0){
                var content =  $.tmpl(this.template_item, server);
                $(li).find('.logHistory').html(content);
                $(li).find('.logHistory li:gt(0)').hide();
            }
            serverList.append(li);
        }
        return this;
    },
    init: function(){
        $.template(this.template_item , '<li>${time} - ${server} - ${host} - ${ping}ms</li>');
        $.template(this.template_log , '<li><a class="exp" href="#">+</a><ul class="logHistory"><li>This ${name} do not have info</li></ul></li>');
        $('#servers_list .exp').live('click', function(e){
            e.preventDefault();
            console.log($(this).parent('li').find('.logHistory li:gt(0)'));
            $(this).parents('li').find('.logHistory li:gt(0)').toggle();
        });
    }
};


var requestor = {

    start: function(){
        //TODO: make cyclic requests
        this.doRequest();
    },

    doRequest:function(){
        $.get('/dashboard', {}, requestor.pushResponse, 'json');
    },

    pushResponse: function(data, textStatus, jqXHR){

        if(typeof(data) != 'object' || textStatus != 'success'){
            alert('request broken');
            return ;
        }

        servers.setData(data['servers']).update();

    }


};


$(document).ready(function(){

    initStubs();

    queue.init();

//    setInterval(function(){
//        $('#queues_list .worker_stats').each(function(){
//            worker.setItem(this).setData().update();
//        });
//    }, 1000);

    servers.init();
    requestor.start();

});
