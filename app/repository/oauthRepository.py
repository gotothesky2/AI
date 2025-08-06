from repository.Repository import BaseRepository
from domain.OAuth import OAuth
from typing import Optional

class OAuthRepository(BaseRepository[OAuth]):
    def __init__(self):
        super().__init__(OAuth)
    
    def findByAccessToken(self, access_token: str) -> Optional[OAuth]:
        """액세스 토큰으로 OAuth 레코드 조회"""
        return self.session.query(OAuth).filter(OAuth.accessToken == access_token).first()
    
    def findByUserId(self, user_id: str) -> list[OAuth]:
        """사용자 ID로 OAuth 레코드 목록 조회"""
        return self.session.query(OAuth).filter(OAuth.uid == user_id).all()
    
    def findByProviderAndUserId(self, provider: str, user_id: str) -> Optional[OAuth]:
        """프로바이더와 사용자 ID로 OAuth 레코드 조회"""
        return self.session.query(OAuth).filter(
            OAuth.provider == provider,
            OAuth.uid == user_id
        ).first()
    
    def deleteExpiredTokens(self) -> int:
        """만료된 토큰들 삭제"""
        from datetime import datetime
        expired_count = self.session.query(OAuth).filter(
            OAuth.expireDate < datetime.now()
        ).count()
        
        self.session.query(OAuth).filter(
            OAuth.expireDate < datetime.now()
        ).delete()
        
        return expired_count

# 싱글톤 인스턴스
oauthRepository = OAuthRepository() 