import praw

# Put your vars here

subreddit = 'coys'

# Canned responses
cans = {
    'rules': 'Removed because posts like this are against the sub rules.'
}

# Specify the keyword and what days they should be removed
weekly_threads = {
    """
    Example:
    'anything': {
        'day': 'Saturday',
        'name': 'Weekly \"anything goes\"'
    }
    """
}

flair_mapping = {
    """
    Example"
    'Text': 'css_class'
    """
}


def post_is_suspicious(post_to_check: praw.objects.Submission) -> bool:
    """
    A function that can be passed a submission to check against and return whether or not it's "suspicious" or otherwise
    deserving of closer attention.

    :type post_to_check: praw.objects.Submission
    :rtype : bool
    :param post_to_check: The Submission instance to check
    :return: True if suspicious, False if now
    """
    return False