
def get_time_delta(timeA, timeB):
    delta = timeB - timeA
    delta = int(delta.total_seconds())
    if delta < 60:
        print '%s s' % delta
        return '%s s' % delta
    elif delta < 60 * 60:
        return '%s min' % (delta/60)
    elif delta < 60 * 60 * 24:
        return '%s h' % (delta/(60 * 60))
    else:
        return '%s day' % (delta/(60 * 60 * 24))
