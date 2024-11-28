import React from "react";


function decodeEntities(encodedString) {
    let textArea = document.createElement('textarea');
    textArea.innerHTML = encodedString;
    return textArea.value;
}

class SpiderButton extends React.Component  {
    render() {
        const style = {
            backgroundColor: "#eff6fa",
            border: "0.1em solid #eff6fa",
            borderRadius: "0.4em",
            boxSizing: "border-box",
            color: "#259",
            cursor: "pointer",
            display: "inline-block",
            fontSize: "0.6em",
            fontWeight: "bold",
            height: "3em",
            width: "92%",
            letterSpacing: "0.1rem",
            lineHeight: "3em",
            padding: "1 4em",
            textAlign: "center",
            textDecoration: "none"
        };

        return (
            <li><div>
            <p>{this.props.desc}</p>
            <a style={style} href={this.props.url} target="_blank">{this.props.title}</a>
            </div></li>
        )
    }
};

class Rank extends React.Component  {
    render() {
        const style = {
            color: "#c6c6c6",
            textAlign: "right",
            fontFamily: "Roboto Mono",
            fontSize: "medium",
            fontWeight: "bold",
            width: "40px",
            paddingRight: "25px",
            flexShrink: 0
        };

        return (
            <span style={style}>
            {this.props.rank}
            </span>
        )
    }
};

class ArticleLink extends React.Component  {
    render() {
        const style = {
            fontFamily: "MiSans",
            fontSize: "0.9em",
            fontWeight: "normal",
            lineHeight: "110%",
            margin: "0px",
            padding: "0px",
        };
        let url = "/a/" + this.props.aid;
        let title = decodeEntities(this.props.title);

        return (
            <span className="articlelink">
            <a style={style} href={url} target="_blank">{title}</a>
            </span>
        )
    }
};

class OrginalLink extends React.Component  {
    render() {
        const style = {
            margin: "0px",
            padding: "0 12px",
            fontSize: "x-small",
        };

        return (
            <span className="articlelink">
            <a style={style} href={this.props.url} target="_blank">🔗</a>
            </span>
        )
    }
};

class DomainLink extends React.Component  {
    render() {
        const style = {
            color: "#888",
            fontSize: "x-small",
            whiteSpace: "nowrap",
            textDecoration: "none",
            margin: "0px",
            padding: "0px",
        };
        let url = "http://" + this.props.domain;

        return (
            <span>
            <a style={style} href={url} target="_blank">({this.props.domain})</a>
            </span>
        )
    }
};

class EntryTitle extends React.Component  {
    render() {
        const style = {
            margin: "0px",
            padding: "0px"
        };

        return (
            <div style={style}>
            <ArticleLink aid={this.props.aid} title={this.props.title} />
            <OrginalLink url={this.props.url} />
            <DomainLink domain={this.props.domain} />
            </div>
        )
    }
};

class SpiderTag extends React.Component  {
    render() {
        const style = {
            color: "#999",
            fontSize: "x-small",
            fontWeight: "bold",
            marginRight: "4px",
            marginBottom: "2px",
            textDecoration: "none"
        };
        let spid = this.props.spider.spid;
        let spname = this.props.spider.spname;
        let url = "/p/" + spid;

        return (
            <span>
            <a style={style} href={url} target="_blank">[{spname}]</a>
            </span>
        )
    }
};

class ArticleTag extends React.Component  {
    render() {
        const style = {
            fontWeight: "normal",
            fontSize: "xx-small",
            color: "#999",
            backgroundColor: "#eee",
            borderRadius: "30px",
            padding: "1px 10px",
            marginRight: "4px",
            marginBottom: "2px",
            whiteSpace: "nowrap"
        };

        return (
            <span style={style}>
            {this.props.tag}
            </span>
        )
    }
};

class EntryTags extends React.Component {
    render() {
        const style = {
            display: "flex",
            flexDirection: "row",
            flexWrap: "wrap",
            alignItems: "baseline",
            margin: "0px",
            padding: "0px",
        };
        let spider = this.props.spider;
        let tags = this.props.tags;

        return (
            <div style={style}>
            <SpiderTag spider={spider} />
            {tags.map(function(tag, index) { return <ArticleTag key={index} tag={tag} />; })}
            </div>
        )
    }
};

class Entry extends React.Component {
    render() {
        const style = {
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            marginBottom: "12px"
        };

        let index = this.props.index;
        let entry = this.props.entry;
        let spider = {spid: entry["spider"], spname: entry["category"]};
        let tags = (entry["tag"] == null) ? [] : entry["tag"];

        return (
            <div style={style}>
            <Rank rank={index} />
            <div>
            <EntryTitle aid={entry["id"]} title={entry["title"]} url={entry["link"]} domain={entry["domain"]} />
            <EntryTags spider={spider} tags={tags} />
            </div>
            </div>
        )
    }
};

class Entries extends React.Component {
    render() {
        let entries = this.props.entries;

        return (
            <div>
            {entries.map(function(entry, index) {
                return <Entry key={index} index={index} entry={entry} />
            })}
            </div>
        )
    }
};

class Hr extends React.Component {
    render() {
        const style = {
            border: "none",
            height: 1,
            color: "#EEE",
            backgroundColor: "#EEE",
            marginBottom: "1em",
            clear: "both"
        };

        return (
            <hr style={style} />
        )
    }
};

class Blank extends React.Component {
    render() {
        const style = {
            minHeight: "1px",
            width: "25%",
            flexShrink: 0
        };

        return (
            <div style={style}></div>
        )
    }
};

class ContentDiv extends React.Component {
    constructor(props) {
        super(props);
    };

    render() {
        const style = {
            display: "flex",
            flexDirection: "row",
            flexWrap: "nowrap",
        };

        return (
            <div>
            <Hr />
            <div style={style}>
            <Blank />
            <Entries entries={this.props.data} />
            <Blank />
            </div>
            <Hr />
            </div>
        )
    }
};

class DayLink extends React.Component {
    onClick(e, day) {
        e.preventDefault();
        e.stopPropagation();

        this.props.onDayLinkClick(day);
    }

    render() {
        let text = "";
        let style = {};

        if (this.props.handType == "handright") {
            text = "⤞";
            style = {
                float: "right"
            }
        }
        else {
            text = "⤝";
            style = {
                float: "left"
            }
        }

        return (
            <span style={style}>
            <a href="#" onClick={(e)=>this.onClick(e, this.props.day)}>
            {text}
            </a>
            </span>
        )
    }
};

class DayLinkDiv extends React.Component {
    render() {
        const style = {
            paddingLeft: "40%",
            paddingRight: "40%"
        };

        return (
            <div style={style}>
            <DayLink handType="handleft" day={this.props.day_after} onDayLinkClick={this.props.onDayLinkClick} />
            <DayLink handType="handright" day={this.props.day_before} onDayLinkClick={this.props.onDayLinkClick} />
            </div>
        )
    }
};

export {ContentDiv, DayLinkDiv};


/* vim: set ts=4 sw=4 sts=4 ft=javascript et: */

