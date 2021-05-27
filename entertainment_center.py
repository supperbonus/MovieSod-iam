import fresh_tomatoes
import media


def main():

    ae = media.Movie("Avengers: EndGame",
                     "The Avengers take a final stand against Thanos",
                     "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_.jpg",
                     "https://www.youtube.com/watch?v=TcMBFSGVi1c",
                     "April 26, 2019")

    ach = media.Movie("Annabelle Comes Home",
                      "Determined to keep Annabelle from wreaking more havoc",
                      "https://m.media-amazon.com/images/M/MV5BYmI4NDNiMmQtZTFkYi00ZDVmLThlYTAtMWJlMjU1M2I2ZmViXkEyXkFqcGdeQXVyNjg2NjQwMDQ@._V1_SY1000_CR0,0,674,1000_AL_.jpg",
                      "https://www.youtube.com/watch?v=EMa-KFfatT0",
                      "June 26, 2019")

    oh = media.Movie("Eternals",
                     "ตลอดหลายปีที่ผ่านมาเราไม่เคยยุ่งเกี่ยวเลยจนถึงตอนนี้",
                     "https://terrigen-cdn-dev.marvel.com/content/prod/1x/online_10.jpg",
                     "https://www.youtube.com/watch?v=0WVDKZJkGlY",
                     "November 5, 2021")

    ou = media.Movie("EVERYTHING,EVERYTHING"
                     "วัยรุ่นที่ใช้ชีวิตแต่ในบ้าน 18 ปีเพราะแพ้ทุกอย่างตกหลุมรักเด็กชายที่ย้ายเข้ามาอยู่ข้างๆ",
                     "https://www.joblo.com/assets/images/oldsite/posters/images/full/everything-everything-poster.jpg",
                     "https://www.youtube.com/watch?v=42KNwQ6u42U",
                     "Mar 17, 2017")

    cd = media.Movie("อ้ายคนหล่อลวง"
                     "มาร่วมต้มกันเป็นแก๊งมาร่วมแกงกันเป็นทีมกับภารกิจตุ๋นเงินล้านงานนี้ทั้งคน หล่อ คน ลวง เตรียมตัวมาล้วงหัวใจคุณ",
                     "https://s359.kapook.com/r/600/auto/pagebuilder/5558e69e-5541-487b-81d1-6cb8cc9979d6.jpg",
                     "https://www.youtube.com/watch?v=lRifyR1jrHw",
                     "Dec 3, 2020")

    ax = media.Movie("Ghostbusters Afterlife"
                     "เมื่อแม่เลี้ยงเดี่ยวและลูก ๆ ทั้งสองมาถึงเมืองเล็กแห่งนี้พวกเขาเริ่มค้นพบความเชื่อมโยงกับโกสต์บัสเตอร์ดั้งเดิมและมรดกลับที่ปู่ทิ้งไว้",
                     "https://cdn.shopify.com/s/files/1/0057/3728/3618/products/ghostbusters-afterlife_cekokhwh_480x.progressive.jpg?v=1613681189",
                     "https://www.youtube.com/watch?v=ahZFCF--uRY",
                     "Mar 17, 2021")

    sm = media.Movie("Spider-Man: FFH",
                     "หลังจากเหตุการณ์ของ Avengers: Endgame",
                     "https://f.ptcdn.info/827/064/000/pu4bgd46z0K6ox1BHyE2-o.jpg",
                     "https://www.youtube.com/watch?v=Nt9L1jCKGnE",
                     "July 5, 2019")

    am = media.Movie("Harry Potter And The Chamber Of Secrets",
                     "แฮร์รี่เพิกเฉยต่อคำเตือนไม่ให้กลับไปที่ฮอกวอตส์เพียงเพื่อพบว่าโรงเรียนถูกโจมตีด้วยการโจมตีลึกลับและเสียงแปลก ๆ หลอกหลอนเขา",
                     "https://cdn.shopify.com/s/files/1/0057/3728/3618/products/e64efa0fb511d173e42b7d5879cb1e7a_4d273617-535c-4969-bb5d-aa9f3a398f3a_480x.progressive.jpg?v=1573591640",
                     "https://www.youtube.com/watch?v=1bq0qff4iF8",
                     "July 5, 2019")

    sr = media.Movie("Scary movie"
                     "เป็นภาพยนตร์ซีรีส์อเมริกันที่ประกอบด้วยภาพยนตร์ล้อเลียนห้าเรื่องที่เน้นไปที่ภาพยนตร์แนวสยองขวัญ",
                     "https://upload.wikimedia.org/wikipedia/en/2/29/Movie_poster_for_%22Scary_Movie%22.jpg",
                     "https://www.youtube.com/watch?v=HTLPULt0eJ4",
                     "Dec 3, 2020")

    ee = media.Movie("Inside out"
                     "มหัศจรรย์อารมณ์อลเวง เป็นภาพยนตร์แอนิเมชันสามมิติแนวดราม่าตลกจากประเทศสหรัฐอเมริกา",
                     "https://lumiere-a.akamaihd.net/v1/images/rich_insideout_header_mobile_ce11b9a6.jpeg?region=0,0,640,952",
                     "https://www.youtube.com/watch?v=seMwpP0yeu4",
                     "May 18, 2015")

    we = media.Movie("Archenemy"
                     "เป็นภาพยนตร์ซีรีส์อเมริกันที่ประกอบด้วยภาพยนตร์ล้อเลียนห้าเรื่องที่เน้นไปที่ภาพยนตร์แนวสยองขวัญ",
                     "https://www.joblo.com/assets/images/joblo/posters/2020/10/archenemyposter.jpg",
                     "https://www.youtube.com/watch?v=5uIUUKZsEUY",
                     "Oct 6, 2020")

    wa = media.Movie("ฉลาดเกมส์โกง"
                     "ลินนักเรียนผลการเรียนดีที่มักจะแอบบอกคำตอบให้กับเพื่อนสนิทอย่างเกรซอยู่เสมอเพราะเธอเป็นนักเรียนสายกิจกรรมที่ไม่ค่อยจะมีความสามารถในด้านนี้สักเท่าไหร่ นอกจากเกรซแล้วยังมีพัฒน์นักเรียนบ้านรวยที่สามารถซื้อทุกอย่างได้ด้วยเงิน",
                     "https://image.bestreview.asia/wp-content/uploads/2021/04/Bad-Genius.jpg",
                     "https://www.youtube.com/watch?v=JcUf9ANCpNY",
                     "May 3, 2017")
    movies = [ae, sm, ach, oh, ou, sr, ax, am, cd, ee, we,wa]
    fresh_tomatoes.open_movies_page(movies)

