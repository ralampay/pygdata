from googleapiclient.discovery import build
#from sklearn.feature_extraction.text import TfidfVectorizer
import re
import json

class FetchYtComments:
    def __init__(self, api_key=None, service_name='youtube', version='v3', video_id=None, debug=False):
        self.api_key                = api_key
        self.comments               = []
        self.comment_ids            = []
        self.published_ats          = []
        self.updated_ats            = []
        self.author_display_names   = []
        self.service_name           = service_name
        self.version                = version
        self.video_id               = video_id
        self.items                  = []
        self.like_counts            = []
        self.debug                  = debug

    def execute(self):
        self.youtube = build(
            self.service_name,
            self.version,
            developerKey=self.api_key
        )

        next_page_token = None

        while True:
            results = self.fetch_comments(
                video_id=self.video_id,
                page_token=next_page_token
            )

            print("Fetched {} comments...".format(len(results["items"])))

            self.build_comments(results)

            next_page_token = results.get("nextPageToken")

            if next_page_token is None:
                break

        return self.comments

    def build_comments(self, results):
        for item in results["items"]:
            if self.debug:
                print(json.dumps(item, indent = 2))

            comment_id          = item["id"]
            comment             = item["snippet"]["topLevelComment"]
            content             = comment["snippet"]["textOriginal"]
            published_at        = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
            updated_at          = item["snippet"]["topLevelComment"]["snippet"]["updatedAt"]
            author_display_name = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]

            # Cleanup
            content = content.lower()
            content = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", content)

            self.comments.append(content)
            self.comment_ids.append(comment_id)
            self.published_ats.append(published_at)
            self.updated_ats.append(updated_at)
            self.author_display_names.append(author_display_name)

            item_data = {
                'video_id':             self.video_id,
                'comment_id':           comment_id,
                'content':              content,
                'published_at':         published_at,
                'updated_at':           updated_at,
                'author_display_name':  author_display_name
            }

            if self.debug:
                print(json.dumps(item_data, indent = 2))

            self.items.append(item_data)

    def fetch_comments(self, video_id=None, page_token=None):
        results = self.youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            pageToken=page_token
        ).execute()

        return results
