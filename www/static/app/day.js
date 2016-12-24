import React from "react";
import { render } from "react-dom";
import {ContentDiv, DayLinkDiv} from "./day_component";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.setDay = this.setDay.bind(this);
    this.onDayLinkClick = this.onDayLinkClick.bind(this);
    this.state = {day_before: null, day_after: null};
  }

  setDay(day) {
    var url = new URL(window.location.origin+"/api/day");
    var params = {day: day};
    Object.keys(params).forEach(
      key => url.searchParams.append(key, params[key])
    );
    var this_ = this;
    fetch(url).then(function(response) {
      return response.json();
    })
    .then(function(data) {
      var err = data["err"];
      if (!err) {
        var nstate = {day_before: data["day_before"],
                      day_after: data["day_after"]};
        if (data["data"]) {
          nstate["data"] = data["data"];
        }
        if (nstate["data"] == null) {
          var now = new Date(document.title);
          var t = new Date();
          var today = new Date(t.getFullYear(), t.getMonth(), t.getDate());
          if (now >= today && nstate["day_before"] != null) {
            this_.setDay(nstate["day_before"]);
            return;
          }
        }
        else {
          document.title = day;
          window.history.pushState(day, day, "/d/" + day);
          this_.setState(nstate);
        }
      }
    })
    .catch(function(err) {
      console.log("error in fetch json data");
    });
  }

  componentWillMount(){
    this.setDay(document.title);
  }

  onDayLinkClick(day) {
    if (day) {
      this.setDay(day);
    }
  }

  render() {
      return (
        <div>
          <ContentDiv data={this.state.data} />
          <DayLinkDiv day_after={this.state.day_after} day_before={this.state.day_before} onDayLinkClick={this.onDayLinkClick} />
        </div>
      )
    }
};

render(<App />, document.getElementById('content'));
