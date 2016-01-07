from django.test import LiveServerTestCase
from selenium import webdriver


# 사이트 체커의 유저스토리를 먼저 작성한다.
class FirstVisitUser(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_visit_and_register_mail_and_site_url(self):
        # 젤리는 커뮤니티에서 간편하게 웹서버 상태를 모니터링 해주는
        # 웹사이트가 있다고 해서 접속해본다.
        self.browser.get(self.live_server_url)

        # 웹페이지의 타이틀은 'sitechecker'다.
        self.assertIn('sitechecker', self.browser.title)

        # Gmail계정과 체크할 URL을 입력하라는 텍스트 박스를 본다.
        nicknamebox = self.browser.find_element_by_id('nickname')
        self.assertEquals(
                nicknamebox.get_attribute('placeholder'),
                'Gmail Nickname'
        )

        urlbox = self.browser.find_element_by_id('siteurl')
        self.assertEquals(
                urlbox.get_attribute('placeholder'),
                'Site URL to Check'
        )

        # 자신의 사이트 모니터링을 위해 구글 아이디를 적고,
        # 체크할 사이트의 URL도 같이 입력한 뒤 추가 버튼을 누른다.
        nicknamebox.send_keys('somesitecheckeruser')
        urlbox.send_keys('jellyms.kr')
        register_button = self.browser.find_element_by_id('register')
        register_button.click()
        # 메일이 등록되었다는 메시지를 본 뒤
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Registered!! Check your email!', page_text)
        # 메일이 왔는지 확인해 보러간다.
        self.fail('pass Functional Test')
