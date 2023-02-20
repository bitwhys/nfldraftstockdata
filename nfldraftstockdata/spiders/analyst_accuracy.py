import scrapy
import re
from nfldraftstockdata.utils.format import remove_instance_of


def parse_analyst_name(raw_string):
    pattern = r"(.*)(\s+-\s+)(.*)"
    publication = ""
    has_publication = re.search(pattern, raw_string)
    if has_publication:
        [analyst_name, _, publication] = has_publication.groups()
        analyst_name = analyst_name.strip()
        publication = publication.strip()
    else:
        analyst_name = raw_string.strip()
    return {"analyst_name": analyst_name, "publication": publication}


def get_mock_year(url):
    year_query_pattern = r"\?year=(\d{4})"
    year = "2022"
    m = re.search(year_query_pattern, url)
    if m:
        [year] = m.groups()
    return year


class AnalystAccuracySpider(scrapy.Spider):
    name = "analyst_accuracy"
    allowed_domains = ["www.fantasypros.com"]
    start_urls = [
        "https://www.fantasypros.com/nfl/accuracy/mock-drafts.php",
        "https://www.fantasypros.com/nfl/accuracy/mock-drafts.php?year=2021",
        "https://www.fantasypros.com/nfl/accuracy/mock-drafts.php?year=2020",
        "https://www.fantasypros.com/nfl/accuracy/mock-drafts.php?year=2019",
        "https://www.fantasypros.com/nfl/accuracy/mock-drafts.php?year=2018",
    ]

    def parse(self, response):
        rows = response.xpath("//tbody/tr")
        year = get_mock_year(response.url)
        for row in rows:
            data = {}
            [_, raw_analyst, *stats] = row.xpath("./td")
            [draft_slots, player_ranks, positions, teams, total_score] = stats
            analyst_str = raw_analyst.xpath("./a/text()").get()
            source_link = raw_analyst.xpath("./a/@href").get()
            data.update({"source_link": source_link})
            data.update(parse_analyst_name(analyst_str))
            data.update({"mock_accuracy": {"year": year}})
            data["mock_accuracy"].update(
                {"draft_slots": draft_slots.xpath("./text()").get()}
            )
            data["mock_accuracy"].update(
                {"player_ranks": player_ranks.xpath("./text()").get()}
            )
            data["mock_accuracy"].update(
                {"positions": positions.xpath("./text()").get()}
            )
            data["mock_accuracy"].update({"teams": teams.xpath("./text()").get()})
            data["mock_accuracy"].update(
                {"total_score": total_score.xpath("./text()").get()}
            )

            yield data
