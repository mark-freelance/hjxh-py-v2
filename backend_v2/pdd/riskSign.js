var encoding = {
    utf8: {
        stringToBytes: function(n) {
            return encoding.bin.stringToBytes(unescape(encodeURIComponent(n)))
        },
        bytesToString: function(n) {
            return decodeURIComponent(escape(t.bin.bytesToString(n)))
        }
    },
    bin: {
        stringToBytes: function(n) {
            for (var r = [], t = 0; t < n.length; t++)
                r.push(255 & n.charCodeAt(t));
            return r
        },
        bytesToString: function(n) {
            for (var r = [], t = 0; t < n.length; t++)
                r.push(String.fromCharCode(n[t]));
            return r.join("")
        }
    }
};

// var second = (function(){
//         var r = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
//           , t = {
//             rotl: function(n, r) {
//                 return n << r | n >>> 32 - r
//             },
//             rotr: function(n, r) {
//                 return n << 32 - r | n >>> r
//             },
//             endian: function(n) {
//                 if (n.constructor == Number)
//                     return 16711935 & t.rotl(n, 8) | 4278255360 & t.rotl(n, 24);
//                 for (var r = 0; r < n.length; r++)
//                     n[r] = t.endian(n[r]);
//                 return n
//             },
//             randomBytes: function(n) {
//                 for (var r = []; n > 0; n--)
//                     r.push(Math.floor(256 * Math.random()));
//                 return r
//             },
//             bytesToWords: function(n) {
//                 for (var r = [], t = 0, o = 0; t < n.length; t++,
//                 o += 8)
//                     r[o >>> 5] |= n[t] << 24 - o % 32;
//                 return r
//             },
//             wordsToBytes: function(n) {
//                 for (var r = [], t = 0; t < 32 * n.length; t += 8)
//                     r.push(n[t >>> 5] >>> 24 - t % 32 & 255);
//                 return r
//             },
//             bytesToHex: function(n) {
//                 for (var r = [], t = 0; t < n.length; t++)
//                     r.push((n[t] >>> 4).toString(16)),
//                     r.push((15 & n[t]).toString(16));
//                 return r.join("")
//             },
//             hexToBytes: function(n) {
//                 for (var r = [], t = 0; t < n.length; t += 2)
//                     r.push(parseInt(n.substr(t, 2), 16));
//                 return r
//             },
//             bytesToBase64: function(n) {
//                 for (var t = [], o = 0; o < n.length; o += 3)
//                     for (var e = n[o] << 16 | n[o + 1] << 8 | n[o + 2], i = 0; i < 4; i++)
//                         8 * o + 6 * i <= 8 * n.length ? t.push(r.charAt(e >>> 6 * (3 - i) & 63)) : t.push("=");
//                 return t.join("")
//             },
//             base64ToBytes: function(n) {
//                 n = n.replace(/[^A-Z0-9+\/]/gi, "");
//                 for (var t = [], o = 0, e = 0; o < n.length; e = ++o % 4)
//                     0 != e && t.push((r.indexOf(n.charAt(o - 1)) & Math.pow(2, -2 * e + 8) - 1) << 2 * e | r.indexOf(n.charAt(o)) >>> 6 - 2 * e);
//                 return t
//             }
//         };
//         n.exports = t
//     }
// )

var tttt = {
    rotl: function(n, r) {
        return n << r | n >>> 32 - r
    },
    rotr: function(n, r) {
        return n << 32 - r | n >>> r
    },
    endian: function(n) {
        if (n.constructor == Number)
            return 16711935 & tttt.rotl(n, 8) | 4278255360 & tttt.rotl(n, 24);
        for (var r = 0; r < n.length; r++)
            n[r] = tttt.endian(n[r]);
        return n
    },
    randomBytes: function(n) {
        for (var r = []; n > 0; n--)
            r.push(Math.floor(256 * Math.random()));
        return r
    },
    bytesToWords: function(n) {
        for (var r = [], t = 0, o = 0; t < n.length; t++,
        o += 8)
            r[o >>> 5] |= n[t] << 24 - o % 32;
        return r
    },
    wordsToBytes: function(n) {
        for (var r = [], t = 0; t < 32 * n.length; t += 8)
            r.push(n[t >>> 5] >>> 24 - t % 32 & 255);
        return r
    },
    bytesToHex: function(n) {
        for (var r = [], t = 0; t < n.length; t++)
            r.push((n[t] >>> 4).toString(16)),
            r.push((15 & n[t]).toString(16));
        return r.join("")
    },
    hexToBytes: function(n) {
        for (var r = [], t = 0; t < n.length; t += 2)
            r.push(parseInt(n.substr(t, 2), 16));
        return r
    },
    bytesToBase64: function(n) {
        for (var t = [], o = 0; o < n.length; o += 3)
            for (var e = n[o] << 16 | n[o + 1] << 8 | n[o + 2], i = 0; i < 4; i++)
                8 * o + 6 * i <= 8 * n.length ? t.push(r.charAt(e >>> 6 * (3 - i) & 63)) : t.push("=");
        return t.join("")
    },
    base64ToBytes: function(n) {
        n = n.replace(/[^A-Z0-9+\/]/gi, "");
        for (var t = [], o = 0, e = 0; o < n.length; e = ++o % 4)
            0 != e && t.push((r.indexOf(n.charAt(o - 1)) & Math.pow(2, -2 * e + 8) - 1) << 2 * e | r.indexOf(n.charAt(o)) >>> 6 - 2 * e);
        return t
    }
};


function third() {
    function t(n) {
        return !!n.constructor && "function" === typeof n.constructor.isBuffer && n.constructor.isBuffer(n)
    }
    n.exports = function(n) {
        return null != n && (t(n) || function(n) {
            return "function" === typeof n.readFloatLE && "function" === typeof n.slice && t(n.slice(0, 0))
        }(n) || !!n._isBuffer)
    }
};

function riskSign(n,t) {
    var r = tttt
      , o = encoding.utf8
      , e = third
      , i = encoding.bin
      , u = function(n, t) {
        n.constructor == String ? n = t && "binary" === t.encoding ? i.stringToBytes(n) : o.stringToBytes(n) : e(n) ? n = Array.prototype.slice.call(n, 0) : Array.isArray(n) || n.constructor === Uint8Array || (n = n.toString());
        for (var s = r.bytesToWords(n), c = 8 * n.length, f = 1732584193, a = -271733879, g = -1732584194, h = 271733878, p = 0; p < s.length; p++)
            s[p] = 16711935 & (s[p] << 8 | s[p] >>> 24) | 4278255360 & (s[p] << 24 | s[p] >>> 8);
        s[c >>> 5] |= 128 << c % 32,
        s[14 + (c + 64 >>> 9 << 4)] = c;
        var l = u._ff
          , y = u._gg
          , v = u._hh
          , d = u._ii;
        for (p = 0; p < s.length; p += 16) {
            var b = f
              , T = a
              , B = g
              , w = h;
            f = l(f, a, g, h, s[p + 0], 7, -680876936),
            h = l(h, f, a, g, s[p + 1], 12, -389564586),
            g = l(g, h, f, a, s[p + 2], 17, 606105819),
            a = l(a, g, h, f, s[p + 3], 22, -1044525330),
            f = l(f, a, g, h, s[p + 4], 7, -176418897),
            h = l(h, f, a, g, s[p + 5], 12, 1200080426),
            g = l(g, h, f, a, s[p + 6], 17, -1473231341),
            a = l(a, g, h, f, s[p + 7], 22, -45705983),
            f = l(f, a, g, h, s[p + 8], 7, 1770035416),
            h = l(h, f, a, g, s[p + 9], 12, -1958414417),
            g = l(g, h, f, a, s[p + 10], 17, -42063),
            a = l(a, g, h, f, s[p + 11], 22, -1990404162),
            f = l(f, a, g, h, s[p + 12], 7, 1804603682),
            h = l(h, f, a, g, s[p + 13], 12, -40341101),
            g = l(g, h, f, a, s[p + 14], 17, -1502002290),
            f = y(f, a = l(a, g, h, f, s[p + 15], 22, 1236535329), g, h, s[p + 1], 5, -165796510),
            h = y(h, f, a, g, s[p + 6], 9, -1069501632),
            g = y(g, h, f, a, s[p + 11], 14, 643717713),
            a = y(a, g, h, f, s[p + 0], 20, -373897302),
            f = y(f, a, g, h, s[p + 5], 5, -701558691),
            h = y(h, f, a, g, s[p + 10], 9, 38016083),
            g = y(g, h, f, a, s[p + 15], 14, -660478335),
            a = y(a, g, h, f, s[p + 4], 20, -405537848),
            f = y(f, a, g, h, s[p + 9], 5, 568446438),
            h = y(h, f, a, g, s[p + 14], 9, -1019803690),
            g = y(g, h, f, a, s[p + 3], 14, -187363961),
            a = y(a, g, h, f, s[p + 8], 20, 1163531501),
            f = y(f, a, g, h, s[p + 13], 5, -1444681467),
            h = y(h, f, a, g, s[p + 2], 9, -51403784),
            g = y(g, h, f, a, s[p + 7], 14, 1735328473),
            f = v(f, a = y(a, g, h, f, s[p + 12], 20, -1926607734), g, h, s[p + 5], 4, -378558),
            h = v(h, f, a, g, s[p + 8], 11, -2022574463),
            g = v(g, h, f, a, s[p + 11], 16, 1839030562),
            a = v(a, g, h, f, s[p + 14], 23, -35309556),
            f = v(f, a, g, h, s[p + 1], 4, -1530992060),
            h = v(h, f, a, g, s[p + 4], 11, 1272893353),
            g = v(g, h, f, a, s[p + 7], 16, -155497632),
            a = v(a, g, h, f, s[p + 10], 23, -1094730640),
            f = v(f, a, g, h, s[p + 13], 4, 681279174),
            h = v(h, f, a, g, s[p + 0], 11, -358537222),
            g = v(g, h, f, a, s[p + 3], 16, -722521979),
            a = v(a, g, h, f, s[p + 6], 23, 76029189),
            f = v(f, a, g, h, s[p + 9], 4, -640364487),
            h = v(h, f, a, g, s[p + 12], 11, -421815835),
            g = v(g, h, f, a, s[p + 15], 16, 530742520),
            f = d(f, a = v(a, g, h, f, s[p + 2], 23, -995338651), g, h, s[p + 0], 6, -198630844),
            h = d(h, f, a, g, s[p + 7], 10, 1126891415),
            g = d(g, h, f, a, s[p + 14], 15, -1416354905),
            a = d(a, g, h, f, s[p + 5], 21, -57434055),
            f = d(f, a, g, h, s[p + 12], 6, 1700485571),
            h = d(h, f, a, g, s[p + 3], 10, -1894986606),
            g = d(g, h, f, a, s[p + 10], 15, -1051523),
            a = d(a, g, h, f, s[p + 1], 21, -2054922799),
            f = d(f, a, g, h, s[p + 8], 6, 1873313359),
            h = d(h, f, a, g, s[p + 15], 10, -30611744),
            g = d(g, h, f, a, s[p + 6], 15, -1560198380),
            a = d(a, g, h, f, s[p + 13], 21, 1309151649),
            f = d(f, a, g, h, s[p + 4], 6, -145523070),
            h = d(h, f, a, g, s[p + 11], 10, -1120210379),
            g = d(g, h, f, a, s[p + 2], 15, 718787259),
            a = d(a, g, h, f, s[p + 9], 21, -343485551),
            f = f + b >>> 0,
            a = a + T >>> 0,
            g = g + B >>> 0,
            h = h + w >>> 0
        }
        return r.endian([f, a, g, h])
    };
    u._ff = function(n, r, t, o, e, i, u) {
        var s = n + (r & t | ~r & o) + (e >>> 0) + u;
        return (s << i | s >>> 32 - i) + r
    }
    ,
    u._gg = function(n, r, t, o, e, i, u) {
        var s = n + (r & o | t & ~o) + (e >>> 0) + u;
        return (s << i | s >>> 32 - i) + r
    }
    ,
    u._hh = function(n, r, t, o, e, i, u) {
        var s = n + (r ^ t ^ o) + (e >>> 0) + u;
        return (s << i | s >>> 32 - i) + r
    }
    ,
    u._ii = function(n, r, t, o, e, i, u) {
        var s = n + (t ^ (r | ~o)) + (e >>> 0) + u;
        return (s << i | s >>> 32 - i) + r
    }
    ,
    u._blocksize = 16,
    u._digestsize = 16;
    if (void 0 === n || null === n)
    throw new Error("Illegal argument " + n);
   // console.log(n)
    var o = r.wordsToBytes(u(n, t));
    //console.log(t && t.asBytes ? o : t && t.asString ? i.bytesToString(o) : r.bytesToHex(o));
    return t && t.asBytes ? o : t && t.asString ? i.bytesToString(o) : r.bytesToHex(o);

}

console.log(riskSign("username=sadsadas&password=NyTTjT8sFc3cV5i&ts=1626797533308"));
