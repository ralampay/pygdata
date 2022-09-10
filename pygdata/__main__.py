import sys
import argparse
import os
from dotenv import dotenv_values
import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from modules.fetch_yt_comments import FetchYtComments

env_vars = dotenv_values(".env")

API_KEY=env_vars.get("API_KEY")

def main():
    mode_choices = [
        "yt-comments"
    ]

    parser = argparse.ArgumentParser(description="PyGData: CMD tool for interacting with Google Data API")

    parser.add_argument("--mode", help="Mode to be used", choices=mode_choices, type=str, default="yt-comments")
    parser.add_argument("--video-id", help="Youtube video id", type=str)
    parser.add_argument("--output-file", help="Output file", type=str, default="data.csv")
    parser.add_argument("--debug", help="Debug flag", type=bool, default=False)

    args        = parser.parse_args()
    mode        = args.mode
    video_id    = args.video_id
    output_file = args.output_file
    debug       = args.debug

    if mode == "yt-comments":
        cmd = FetchYtComments(
            api_key=API_KEY, 
            video_id=video_id, 
            debug=debug
        )

        cmd.execute()

        if output_file:
            data = []

            for item in cmd.items:
                data.append([
                    item['comment_id'],
                    item['content'],
                    item['published_at'],
                    item['updated_at'],
                    item['author_display_name'],
                    item['video_id']
                ])

            columns = [
                'comment_id',
                'content',
                'published_at',
                'updated_at',
                'author_display_name',
                'video_id'
            ]

            df = pd.DataFrame(data, columns=columns)

            if debug:
                print(df)

            df.to_csv(output_file, index=False)

    print("Done.")

if __name__ == '__main__':
    main()
