var ExampleSocket = {
    onMessageCallback: null,
    closedStatuses: [WebSocket.CLOSED, WebSocket.CLOSING],

    init: function(user_id, callback) {
        this.TIMEOUT = 500;
        this.user_id = user_id;

        // TODO Use ssl here to secure communications
        var WEBSOCKET_URL = 'ws://localhost:8888/websocket/' + this.user_id;

        this.websocket = new WebSocket(WEBSOCKET_URL);
        this.onMessageCallback = callback;

        this.websocket.onmessage = function(e) {
            this.onMessageCallback(JSON.parse(e.data));
        }.bind(this);

        this.websocket.onopen = function(e) {
            this.retry_times = 0;
        }.bind(this);

        // If the connection is lost, we try to connect again
        // It happens in development when Tornado gets reloaded
        // or in production when you upload code and restart
        // supervisor if It's needed
        this.websocket.onclose = this.waitForWebsocketConnection.bind(this);
        this.websocket.onerror = this.waitForWebsocketConnection.bind(this);

        return this;
    },

    waitForWebsocketConnection: function(callback) {
        if (this.isOpen()) {
            this.executeCallback(callback);
        } else {
            if (this.isClosed()) {
                this.retry_times++;
                this.init(this.user_id, this.onMessageCallback);
            }

            setTimeout(function () {
                this.waitForWebsocketConnection(callback);
            }.bind(this), this.TIMEOUT * this.retry_times);
        }
    },

    send: function(msg) {
        var self = this;

        self.waitForWebsocketConnection(function() {
            self.websocket.send(JSON.stringify(msg));
        });

        return this;
    },

    executeCallback: function(callback) {
        if (typeof callback === "function") {
            callback();
        }
    },

    isClosed: function() {
        return this.closedStatuses.indexOf(this.websocket.readyState) != -1;
    },

    isOpen: function() {
        return this.websocket.readyState === WebSocket.OPEN;
    }
};
