

var initStubs = function(){

    $('.add_worker').live('click', function(e) {
        e.preventDefault();
        alert("Not Ready Yet");
    });

    $('.stop_worker, .restart_worker, .delete_worker').live('click', function(e) {
        e.preventDefault();
        alert("Not Ready Yet");
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
    get_id: function(){
        return $(this.item).attr('id').split('_').slice(-1);
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

    get_all: function(){
        return $('#queues_list .worker_stats');
    },


    update: function(){
        var wdata = $(this.item).data('worker-data');

        $(this.item).find('.worker_stats .cpu_value').html('' + wdata.cpu + '%').end()
            .find('.worker_stats .mem_value').html('' + wdata.mem + '%').end();
//            .find('.worker_stats .task_value').html(wdata.task_value).end();

        $(this.item).find('.worker_stats .cpu.progress').width(Math.min(Math.max(wdata.cpu, 1), 99)+'%');
        $(this.item).find('.worker_stats .memory.progress').width(Math.min(Math.max(wdata.mem, 1), 99)+'%');

        var counter = $(this.item).data('counter') || 0;

        var cpu_points = this.appendPoint($(this.item).data('cpu-points'), counter, wdata.cpu);
        $(this.item).data('cpu-points', cpu_points);
        
        var mem_points = this.appendPoint($(this.item).data('memory-points'), counter, wdata.mem);
        $(this.item).data('memory-points', mem_points);

//        var task_points = this.appendPoint($(this.item).data('task-points'), counter, wdata.task_value);
//        $(this.item).data('task-points', task_points);

        $(this.item).data('counter', counter + 1);

        $.plot($(this.item).find('.graph_holder_worker'), [
            {
                data: cpu_points,
                lines: {show:true, fill:true},
                color: "rgb(0,255,0)"
            },{
                data: mem_points,
                lines: {show:true, fill:true},
                color: "rgb(22,150,255)"
            }
        ]);

        return this;
    },
    
    setData: function(d){

        for (i in d){
            if( typeof d[i] == 'object'){
                $(this.item).data('worker-data', d[i]);
                break;
            }
        }

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

    get_all: function(){
        return $('#queues_list .queue_details');
    },

    get_id: function(){
        return $(this.item).attr('id').split('_').slice(-2);
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
        var qdata = $(this.item).data('queue-data');

        var counter = $(this.item).data('counter') || 0;

        $(this.item)
            //.find('.queue_stats .cpu_value, .queue_headline .cpu_value').html('' + qdata.cpu_value + '%').end()
            //.find('.queue_stats .mem_value, .queue_headline .mem_value').html('' + qdata.memory_value + '%').end()
            .find('.queue_stats .workers_value, .queue_headline .workers_value').html(qdata.params.workers).end();

//        $(this.item).find('.queue_stats .cpu.progress').width(Math.min(Math.max(qdata.cpu_value, 1), 99)+'%');
//        $(this.item).find('.queue_stats .memory.progress').width(Math.min(Math.max(qdata.memory_value, 1), 99)+'%');
        
        var run_points = this.appendPoint($(this.item).data('run_points'), counter, qdata.params.running);
        $(this.item).data('run_points', run_points);

        var queued_points = this.appendPoint($(this.item).data('queued_points'), counter, qdata.params.queued);
        $(this.item).data('queued_points', queued_points);

        $(this.item).data('counter', counter + 1);

        $.plot($(this.item).find('.graph_holder_queue'), [
            {
                data: run_points,
                lines: {show:true, fill:true},
                color: "rgb(0,255,0)"
            },{
                data: queued_points,
                lines: {show:true, fill:true},
                color: "rgb(22,150,255)"
            }
        ]);
        
        return this;
    },

    initGraph: function(){
        
    },

    setData: function(d){
//        //this is stub
//        var d = {
//            cpu_value: Math.round(Math.random() * 100),
//            memory_value: Math.round(Math.random() * 100),
//            workers_value: Math.round(Math.random() * 10)
//        };
        
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
    template_item: 'serverLogItem',

    setData: function(data){
        this.data = data;
        return this;
    },
    
    update: function(){
        var serverList = $('#servers').find('#servers_list');

        for(i in this.data){
            var server = this.data[i];

            if(server.records.length > 0){
                var content =  $.tmpl(this.template_item, server.records);
                serverList.find('#server_' + server.id + ' .logHistory').prepend(content);
                serverList.find('#server_' + server.id + ' .logHistory li:gt(10)').remove();
            }
        }
        return this;
    },
    init: function(){
        $.template(this.template_item , '<li>${time} - ${server} - ${host} - ${ping}ms</li>');
        $('#servers_list .exp').live('click', function(e){
            e.preventDefault();
            var history = $(this).parents('li').find('.logHistory');
            if ($(history).hasClass('collapsed')){
                $(history).removeClass('collapsed');
            }else{
                $(history).addClass('collapsed');
            }

        });
    }
};


var supervisords = {

    data: null,
    template_item: 'supervisorLogItem',

    setData: function(data){
        this.data = data;
        return this;
    },

    update: function(){
        var svList = $('#supervisords').find('#supervisords_list');

        for(i in this.data){
            var sv = this.data[i];

            if(sv.length > 0){
                var content =  $.tmpl(this.template_item, sv);
                svList.find('#supervisord_' + i + ' .logHistory').prepend(content);
                svList.find('#supervisord_' + i + ' .logHistory li:gt(10)').remove();
            }
        }
        return this;
    },
    init: function(){
        $.template(this.template_item , '<li><span class="err_${level}">${level}</span> ${time} - <span class="state_${params.state}">${params.state} PID:${params.pid} </span> - ${params.name}:${params.group} </li>');
        $('#supervisords_list .exp').live('click', function(e){
            e.preventDefault();
            var history = $(this).parents('li').find('.logHistory');
            if ($(history).hasClass('collapsed')){
                $(history).removeClass('collapsed');
            }else{
                $(history).addClass('collapsed');
            }

        });
    }
};


var requestor = {

    start: function(){
        //TODO: make cyclic requests
        requestor.doRequest();
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

        supervisords.setData(data['supervisords']).update();

        var workers = worker.get_all().toArray();
        for (i in workers){
            var wobj = worker.setItem(workers[i]);
            wobj.setData(data['workers'][wobj.get_id()]).update();
        }


        var qList = queue.get_all().toArray();
        for(i in qList){
            var qItem = queue.setQueue(qList[i]);
            var ids = queue.get_id();
            qItem.setData(data['gearmans'][ids[0]]['stats'][ids[1]]).update();
        }
    },

    init: function(){
        requestor.start();
        setInterval(requestor.start, 5000);
    }


};


$(document).ready(function(){

    initStubs();

    queue.init();

    servers.init();
    requestor.init();
    supervisords.init();

});
