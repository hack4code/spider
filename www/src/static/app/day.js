import React from "react";
import {render} from "react-dom";
import {ContentDiv, DayLinkDiv} from "./day_component";
import "whatwg-fetch";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.setDay = this.setDay.bind(this);
    this.onDayLinkClick = this.onDayLinkClick.bind(this);
    this.state = {day_before: null, day_after: null, data: []};
  }

  setDay(day) {
    let url = new URL(window.location.protocol + "//" + window.location.hostname + "/api/day");
    let params = {day: day}
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    let that = this;

    fetch(url).then(function(response) {
      response.json().then(function(data) {
        if (response.status == 200) {
          let nstate = {day_before: data["day_before"],
                        day_after: data["day_after"]};
          if (data["data"]) {
            nstate["data"] = data["data"];
          }
          const t = new Date();
          const today = new Date(t.getFullYear(), t.getMonth(), t.getDate());
          if (nstate["data"] == null) {
            const now = new Date(document.title);
            if (now >= today && nstate["day_before"] != null) {
              that.setDay(nstate["day_before"]);
              return;
            }
          }
          else {
            document.title = day;
            that.setState(nstate);
            const now = new Date(day);
            if ((now.getFullYear() == today.getFullYear()) && (now.getMonth() == today.getMonth()) && (now.getDate() == today.getDate())) {
                return;
            }
            window.history.pushState(day, day, "/d/" + day);
          }
        }
        else {
          console.log(data['message']);
        }
      })
    })
    .catch(function(err) {
      console.log("fetch error");
    })
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

render(<App />, document.getElementById("content"));


/* vim: set ts=4 sw=4 sts=4 ft=javascript et: */

