import random, string, email

requires=['PostfixCourier']

def test(ctx):
    PostfixCourier = ctx.modules['PostfixCourier']
    token = ''.join(random.choice(string.letters) for i in xrange(32)).lower()
    msg = PostfixCourier.roundtrip(ctx, token)
    if token == msg[-1]:
        ctx.logger.debug("unfiltered email sent and received correctly")
    else:
        ctx.fail("token-compare", "sent (%s) got (%s)" % (token, msg[-1]))
    
    spamuuid = ctx.conn.rpc.create(classid="Mail:SpamAssassin",
                                   objectid="SpamAssassin",
                                   parentid=ctx.mailuuid, 
                                   data = dict(label_at=str(-50.0), drop_at=str(1000))
                                  )['body']['data']['objid']
    
    ctx.logger.debug('created Mail:SpamAssassin (-50/1000) for %s (%s)' % (ctx.domain, ctx.mailuuid))
    
    # fresh token
    token = ''.join(random.choice(string.letters) for i in xrange(32)).lower()
    msg = PostfixCourier.roundtrip(ctx, token, "no-retr-label")
    parsedmsg = email.message_from_string('\n'.join(msg))
    if not token in msg:
        ctx.fail("token-compare-label", "sent %(s), not found in output" % (token))
    if parsedmsg.get("X-Spam-FLAG") != 'YES':
        ctx.fail("label-yes","expected X-Spam-FLAG: YES, got (%s)" % parsedmsg.get("X-Spam-FLAG"))
    ctx.logger.debug("label test ok (%s)" % parsedmsg.get("X-Spam-FLAG"))
    
    ctx.conn.rpc.update(classid="Mail:SpamAssassin",
                        objectid=spamuuid,
                        data = dict(label_at=str(50.0), drop_at=str(1000)))

    # fresh token
    token = ''.join(random.choice(string.letters) for i in xrange(32)).lower()
    msg = PostfixCourier.roundtrip(ctx, token, "no-retr-nolabel")
    parsedmsg = email.message_from_string('\n'.join(msg))
    if not token in msg:
        ctx.fail("token-compare-nolabel", "sent %(s), not found in output" % (token))
    if parsedmsg.get("X-Spam-FLAG"):
        ctx.fail("label-yes","expected no X-Spam-FLAG, got (%s)" % parsedmsg.get("X-Spam-FLAG"))
    ctx.logger.debug("label test ok (%s)" % parsedmsg.get("X-Spam-FLAG"))

    ctx.conn.rpc.update(classid="Mail:SpamAssassin",
                        objectid=spamuuid,
                        data = dict(label_at=str(5.0), drop_at=str(10)))

    # use GTUBE to get a score of 1000
    gtube = "XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X"
    msg = PostfixCourier.roundtrip(ctx, gtube)
    if msg:
        ctx.fail("drop", "message not dropped")
    ctx.logger.debug("drop test ok")

def cleanup(ctx):
    pass