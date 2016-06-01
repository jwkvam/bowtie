import Plotly from 'plotly.js';

class PlotlyPlot extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.props.initState;
    }

    // changeAll = (all) => {this.setState(all);}
    //

    shouldComponentUpdate(nextProps) {
        return true;
    }

    componentDidMount() {
        // let {data, layout, config} = this.props;
        // if (this.props.onClick)
        if (this.props.onClick)
            this.container.on('plotly_click', function (data) {
                socket.emit(this.props.uuid + '#click', data);
            });
        if (this.props.onBeforeHover)
            this.container.on('plotly_beforehover', function (data) {
                socket.emit(this.props.uuid + '#beforehover', data);
            });
        if (this.props.onHover)
            this.container.on('plotly_hover', function (data) {
                socket.emit(this.props.uuid + '#hover');
            });
        if (this.props.onUnHover)
            this.container.on('plotly_unhover', function (data) {
                socket.emit(this.props.uuid + '#unhover');
            });
        if (this.props.onSelected)
            this.container.on('plotly_selected', function (data) {
                socket.emit(this.props.uuid + '#selected');
            });

        socket.on(this.props.uuid + '#' + 'all', (data) => {
            this.setState(data);
            console.log('hello???')
        });
        Plotly.newPlot(this.container, this.state.data, this.state.layout); //, config);
    }

    // updateState(state) {
    //     console.log('updating...');
    //     this.state = state;
    // }

    // updateState = (ev) => this.setState({ text: ev.target.value });
    

    componentDidUpdate() {
        //TODO use minimal update for given changes
        // this.container.data = this.props.data;
        // this.container.layout = this.props.layout;
        console.log('did update');
        console.log(this.state);
        Plotly.newPlot(this.container, this.state.data, this.state.layout);
    }

    componentWillUnmount() {
        this.container.removeAllListeners('plotly_click');
        this.container.removeAllListeners('plotly_beforehover');
        this.container.removeAllListeners('plotly_hover');
        this.container.removeAllListeners('plotly_unhover');
        this.container.removeAllListeners('plotly_selected');
    }

    render() {
        return (
            <div ref={(node) => this.container=node} />
        );
    }

}

PlotlyPlot.propTypes = {
    uuid: React.PropTypes.string,
    initState: React.PropTypes.object
};

    // onClick: React.PropTypes.func,
    // onBeforeHover: React.PropTypes.func,
    // onHover: React.PropTypes.func,
    // onUnHover: React.PropTypes.func,
    // onSelected: React.PropTypes.func
