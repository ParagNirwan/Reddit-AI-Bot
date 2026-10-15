# Reddit AI Bot

A Python command-line bot that schedules generated Reddit posts and can optionally run a recurring commenting task for a selected subreddit.

## Features

- Schedule a generated post at a daily time supplied in 24-hour `HH:MM` format.
- Optionally schedule subreddit commenting.
- Keep the scheduler running until interrupted by the user.

## Requirements

- Python 3
- Python packages imported by the project, including `schedule` and libraries used for text generation and Reddit API access

Install dependencies from a dependency file if available, or review the imports in the source files and install the required packages.

## Configuration and run

The application prompts for the daily posting time and whether commenting should be enabled:

```bash
python Main.py
```

Configure Reddit API credentials and any AI-provider credentials through environment variables or a local, untracked configuration file. Never commit API keys, refresh tokens, or account passwords.

## Responsible use

Automated posting and commenting must comply with Reddit's current API terms, rate limits, subreddit rules, and spam policies. Test carefully before enabling recurring actions. The scheduler is a simple long-running process and does not provide a durable job queue or monitoring by itself.