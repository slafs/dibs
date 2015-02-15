/** @jsx React.DOM */
'use strict';

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var Message = React.createClass({

    close: function() {
        var node = this.refs.message.getDOMNode();
        $(node).fadeOut();
    },
    render: function() {
        return (
            <div ref="message" className="ui message {this.props.className}">
                <i className="close icon" onClick={this.close}></i>
                {this.props.children}
            </div>
        );
    }
});


/****
    an Item can be **locked** or **unlocked** depending on some server conditions.

    clicking a button sends a POST request. if it's done then it refreshes/rerenders
    itself by calling refreshItem.

    an initial item list (on ItemList) looks like this:

    [
        {"id": 1372, "url": "http://127.0.0.1:8000/api/v1/items/1372/", "name": "item 1" , "locked_by": null, "desc": null, "can_be_locked": null, "created": "2014-10-25T15:33:33.625", "modified": "2014-10-25T15:33:33.625"},
        {"id": 1364, "url": "http://127.0.0.1:8000/api/v1/items/1364/", "name": "item 2" , "locked_by": null, "desc": null, "can_be_locked": null, "created": "2014-10-25T15:33:32.532", "modified": "2014-10-25T15:33:32.533"},
        {"id": 1355, "url": "http://127.0.0.1:8000/api/v1/items/1355/", "name": "item 3" , "locked_by": {"username": "slafs", "first_name": "", "last_name": ""}, "desc": null, "can_be_locked": null, "created": "2014-10-25T15:33:31.298", "modified": "2014-10-25T15:33:31.298"},
        ...
    ]

*/

var Item = React.createClass({

    itemErrorMsgs: {
        forbidden_lock: 'You can\'t lock this item',
        forbidden_unlock: 'You can\'t unlock this item'
    },

    getInitialState: function() {
        return {
            // if item is locked
            locked: this.props.locked_by ? true : false,
            // if we are waiting for lock/unlock
            is_syncing: false,
            // who locked the item
            locked_by: this.props.locked_by,
            // errors while trying to lock/unlock
            errors: []
        }
    },

    refreshItem: function() {
        var req = $.get(this.props.url);

        req.done(function(data) {
            this.setState({
                is_syncing: false,
                locked_by: data.locked_by,
                locked:  data.locked_by ? true : false
            });
        }.bind(this));

        req.fail(function (data, status, headers) {
            console.error("error refresh " + status);
        }.bind(this));

        req.always(function () {
            this.setState({
                is_syncing: false
            })
        }.bind(this));
    },

    lockItem: function(command) {
        this.setState({is_syncing: true});

        var req = $.ajax({
            type: 'POST',
            url: this.props.url + command + '/',
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });

        req.done(function(data) {
            this.refreshItem();
        }.bind(this));

        req.fail(function(xhr) {
            var errors = this.state.errors;
            if (xhr.status == 403) {
                var new_errors = errors.concat([this.itemErrorMsgs["forbidden_" + command]]);
                this.setState({                    errors: new_errors
                });
            }
            this.setState({
                is_syncing: false
            });

        }.bind(this));

        return req;
    },

    render: function() {
        var buttonClasses = "ui " + (this.state.locked ? "red" : "primary") + " button" + (this.state.is_syncing ? " disabled": "");
        var headerClasses = "ui top attached " + (this.state.locked ? "red" : "green") + " label";
        var lock_button = this.state.locked ?
                            <button onClick={this.lockItem.bind(null, 'unlock')} className={buttonClasses}><i className="icon unlock"></i>Unlock</button>
                            :
                            <button onClick={this.lockItem.bind(null, 'lock')} className={buttonClasses}><i className="icon lock"></i>Lock</button>
                            ;
        var errorMsgs = this.state.errors.map(function(error, index) {
            return (
                <Message key={index} className="error">{error}</Message>
            );
        });
        console.log('errors ', errorMsgs);

        return (
            <div className="four wide column">
                    <div className="ui segment">
                        <div className={headerClasses}>{this.props.name}</div>
                        <br/>
                        <p> {this.props.desc} </p>
                        {errorMsgs}
                        {lock_button}
                        <br/>
                        <br/>
                        <br/>
                        {this.state.locked ? <div className="ui bottom attached label">Locked by: {this.state.locked_by}</div> : ''}
                    </div>
            </div>
        )
    }
});

var ItemList = React.createClass({

    listenForItemChanges: function() {
        var sse = new EventSource('/stream');
        var index = null;
        sse.addEventListener('itemChange', function (e) {
            // e.data has an item identifier
            index = this.state.items.findIndex(function(element) {
                return (element.id.toString() === e.data);
            }.bind(this));
            if (index !== null) {
                // ??????????????? what now?
                console.log("item " + index + " should be rendered");
            }
        });
        return sse;
    },

    componentDidMount: function() {
        this.sse = this.listenForItemChanges();
    },
    render: function() {
        var items = [];

        if (!this.props.itemsAreLoading) {

            items = this.props.items.map(function(item) {
                return (
                    <Item key={item.id} {...item}/>
                )
            });
        }
        return (
            <div className="ui page grid">
                {this.props.itemsAreLoading ? <p>Loading...</p> : items}
            </div>
        );
    }
});

var DibsApp = React.createClass({

    getInitialState: function() {
        return {
            items: [],
            items_are_loading: true
        };
    },
    componentDidMount: function() {
        this.req = this.getItems();
    },
    componentWillUnmount: function () {
        this.req.abort();
    },
    getItems: function() {
        var req = $.get(this.props.items_url, this.props.items_url_args);

        req.done(function(data) {
            this.setState({
                items: data
            });
        }.bind(this));

        req.fail(function(data) {
            this.setState({
                items: []
            });
        }.bind(this));

        req.always(function(data) {
            this.setState({
                items_are_loading: false
            });
        }.bind(this));

        return req;
    },
    render: function() {
        return (
            <ItemList items={this.state.items} itemsAreLoading={this.state.items_are_loading} />
        );
    }
});

var container = document.getElementById('main_container');

React.render(
    <DibsApp items_url="/api/v1/items/" />,
    container
);
