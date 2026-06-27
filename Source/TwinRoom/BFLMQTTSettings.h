// Copyright 2026 Andrew Bindraw. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"

#include "MQTTShared.h"
#include "MQTTClientSettings.h"

#include "BFLMQTTSettings.generated.h"

/**
 * 
 */
UCLASS()
class TWINROOM_API UBFLMQTTSettings : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintPure, Category = "MQTT|Settings")
	static FMQTTURL GetMQTTURL();

	UFUNCTION(BlueprintCallable, Category = "MQTT|Settings")
	static void SetMQTTURL(const FMQTTURL& InUrl);

	UFUNCTION(BlueprintPure, Category = "MQTT|Settings")
	static int32 GetPublishRate();

	UFUNCTION(BlueprintCallable, Category = "MQTT|Settings")
	static void SetPublishRate(int32 PublishRate);

	UFUNCTION(BlueprintPure, Category = "MQTT|Settings")
	static bool IsTLSVerifyServerCertificate();

	UFUNCTION(BlueprintCallable, Category = "MQTT|Settings")
	static void SetIsTLSVerifyServerCertificate(bool bIsVerify);

	UFUNCTION(BlueprintPure, Category = "MQTT|Settings")
	static FString GetTLSCertificateAuthorityFile();

	UFUNCTION(BlueprintCallable, Category = "MQTT|Settings")
	static void SetTLSCertificateAuthorityFile(const FString& FullPathToCAFile);

	UFUNCTION(BlueprintCallable, Category = "MQTT|Settings")
	static void SaveMQTTSettings();
};
